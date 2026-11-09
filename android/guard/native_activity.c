/* SPDX-License-Identifier: MIT.
 * Android NativeActivity platform adapter only: one-tap sandbox diagnostic.
 * The freestanding C11 kernel has no libc or Android imports.
 * No Firebird engine, SQL queries, credentials or network are used.
 */
#include <android/native_activity.h>
#include <android/native_window.h>
#include <android/input.h>
#include <android/looper.h>
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include "beta_suite.h"

static ANativeActivity *active_activity;
static ANativeWindow *active_window;
static AInputQueue *active_queue;
static ALooper *active_looper;
static raf_beta_report last_report;
static int executed;
static int receipt_ok;

static const uint8_t *letter(char c) {
    static const uint8_t a[7]={14,17,17,31,17,17,17};
    static const uint8_t e[7]={31,16,16,30,16,16,31};
    static const uint8_t f[7]={31,16,16,30,16,16,16};
    static const uint8_t i[7]={31,4,4,4,4,4,31};
    static const uint8_t l[7]={16,16,16,16,16,16,31};
    static const uint8_t n[7]={17,25,21,19,17,17,17};
    static const uint8_t o[7]={14,17,17,17,17,17,14};
    static const uint8_t p[7]={30,17,17,30,16,16,16};
    static const uint8_t r[7]={30,17,17,30,20,18,17};
    static const uint8_t s[7]={15,16,16,14,1,1,30};
    static const uint8_t t[7]={31,4,4,4,4,4,4};
    static const uint8_t u[7]={17,17,17,17,17,17,14};
    static const uint8_t blank[7]={0,0,0,0,0,0,0};
    switch(c) {
        case 'A':return a;case 'E':return e;case 'F':return f;case 'I':return i;
        case 'L':return l;case 'N':return n;case 'O':return o;
        case 'P':return p;case 'R':return r;case 'S':return s;
        case 'T':return t;case 'U':return u;default:return blank;
    }
}

static void text_line(ANativeWindow_Buffer *b,const char *word,int x,int y,
                      int scale,uint32_t color) {
    const char *p=word;
    if(!b || !word || !b->bits || scale<1) return;
    while(*p) {
        const uint8_t *rows=letter(*p++);
        int r,c,dy,dx;
        for(r=0;r<7;r++) for(c=0;c<5;c++) {
            if(!(rows[r] & (1u << (4-c)))) continue;
            for(dy=0;dy<scale;dy++) for(dx=0;dx<scale;dx++) {
                int xx=x+c*scale+dx,yy=y+r*scale+dy;
                if(xx>=0 && yy>=0 && xx<b->width && yy<b->height)
                    ((uint32_t*)b->bits)[yy*b->stride+xx]=color;
            }
        }
        x+=6*scale;
    }
}

static void draw(void) {
    ANativeWindow_Buffer b;
    uint32_t *pixels;
    int x,y,s;
    if(!active_window) return;
    if(ANativeWindow_setBuffersGeometry(active_window,0,0,WINDOW_FORMAT_RGBA_8888)!=0) return;
    if(ANativeWindow_lock(active_window,&b,0)!=0) return;
    pixels=(uint32_t*)b.bits;
    if(pixels && b.width>0 && b.height>0 && b.stride>=b.width) {
        for(y=0;y<b.height;y++) {
            for(x=0;x<b.width;x++) {
                uint32_t color=0xff182430u;
                if(y<b.height/5) color=0xff253f5fu;
                if(y>b.height*3/4) color=0xff30415bu;
                pixels[y*b.stride+x]=color;
            }
        }
        s=b.width/140;
        if(s<2)s=2;
        if(s>5)s=5;
        text_line(&b,"TAP TO RUN",(b.width-10*6*s)/2,b.height/12,s,0xffffffffu);
        if(executed) {
            uint32_t i;
            text_line(&b,last_report.failed?"FAIL":"PASS",b.width/10,b.height/3,s*2,
                      last_report.failed?0xffff5555u:0xff4cdd9fu);
            text_line(&b,receipt_ok?"FILE PASS":"FILE FAIL",b.width/10,b.height*2/5,s,
                      receipt_ok?0xff4cdd9fu:0xffff5555u);
            for(i=0u;i<last_report.count;i++) {
                int col=(int)(i%6u), row=(int)(i/6u);
                int left=b.width/8+col*b.width/8;
                int top=b.height/2+row*b.height/18;
                int h=b.height/28;
                for(y=top;y<top+h && y<b.height;y++)
                    for(x=left;x<left+b.width/12 && x<b.width;x++)
                        if(y>=0 && x>=0) pixels[y*b.stride+x]=last_report.cases[i].pass?
                             0xff24ae78u:0xffbc4040u;
            }
        }
    }
    (void)ANativeWindow_unlockAndPost(active_window);
}

static int persist(const raf_beta_report *report) {
    char path[512];
    FILE *out;
    uint32_t i;
    int ok=1;
    if(!active_activity || !active_activity->internalDataPath || !report) return 0;
    if(snprintf(path,sizeof(path),"%s/betatester-%08x.csv",
                active_activity->internalDataPath,report->seed)
       >=(int)sizeof(path)) return 0;
    out=fopen(path,"wx");
    if(!out) return 0; /* collision or inaccessible storage = FAIL evidence */
    if(fprintf(out,"schema;seed;scope;physical;engine\n1;%u;gate_sandbox;UNVERIFIED;NOT_RUN\n",
               report->seed)<0) ok=0;
    if(fprintf(out,"case_id;route;status\n")<0) ok=0;
    for(i=0u;i<report->count;i++)
        if(fprintf(out,"GATE_%02u;%u;%s\n",i,report->cases[i].route,
                   report->cases[i].pass?"PASS":"FAIL")<0) ok=0;
    if(fprintf(out,"summary;pass=%u;fail=%u\n",report->passed,report->failed)<0) ok=0;
    if(fclose(out)!=0) ok=0;
    return ok;
}

static void run_once(void) {
    struct timespec ts;
    uint32_t seed=UINT32_C(0x62a4b123);
    if(clock_gettime(CLOCK_MONOTONIC,&ts)==0)
        seed^=(uint32_t)ts.tv_nsec^(uint32_t)ts.tv_sec;
    raf_beta_run(&last_report,seed);
    executed=1;
    receipt_ok=persist(&last_report);
    draw();
}

static int on_input(int fd,int events,void *data) {
    AInputEvent *event;
    (void)fd;(void)events;(void)data;
    if(!active_queue)return 1;
    while(AInputQueue_getEvent(active_queue,&event)>=0) {
        int handled=0;
        if(AInputQueue_preDispatchEvent(active_queue,event))continue;
        if(AInputEvent_getType(event)==AINPUT_EVENT_TYPE_MOTION &&
           (AMotionEvent_getAction(event)&AMOTION_EVENT_ACTION_MASK)==AMOTION_EVENT_ACTION_UP) {
            run_once();
            handled=1;
        }
        AInputQueue_finishEvent(active_queue,event,handled);
    }
    return 1;
}

static void on_queue_created(ANativeActivity *a,AInputQueue *queue) {
    (void)a;
    active_queue=queue;
    active_looper=ALooper_forThread();
    if(!active_looper)active_looper=ALooper_prepare(ALOOPER_PREPARE_ALLOW_NON_CALLBACKS);
    if(active_looper) AInputQueue_attachLooper(queue,active_looper,1,on_input,0);
}
static void on_queue_destroyed(ANativeActivity *a,AInputQueue *queue) {
    (void)a;
    if(active_looper) AInputQueue_detachLooper(queue);
    active_queue=0;
    active_looper=0;
}
static void on_window_created(ANativeActivity *a,ANativeWindow *w) {
    (void)a;active_window=w;draw();
}
static void on_window_destroyed(ANativeActivity *a,ANativeWindow *w) {
    (void)a;(void)w;active_window=0;
}
static void on_activity_destroyed(ANativeActivity *a) {
    (void)a;active_activity=0;active_window=0;
}
__attribute__((visibility("default")))
void ANativeActivity_onCreate(ANativeActivity *a,void *saved,size_t count) {
    (void)saved;(void)count;
    if(!a || !a->callbacks) return;
    active_activity=a;
    a->callbacks->onInputQueueCreated=on_queue_created;
    a->callbacks->onInputQueueDestroyed=on_queue_destroyed;
    a->callbacks->onNativeWindowCreated=on_window_created;
    a->callbacks->onNativeWindowResized=on_window_created;
    a->callbacks->onNativeWindowRedrawNeeded=on_window_created;
    a->callbacks->onNativeWindowDestroyed=on_window_destroyed;
    a->callbacks->onDestroy=on_activity_destroyed;
}
