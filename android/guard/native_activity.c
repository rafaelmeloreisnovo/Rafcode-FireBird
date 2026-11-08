/* SPDX-License-Identifier: MIT.
 * Android-only UI entry, unrelated to the Firebird database engine.
 * Core is independently compiled C11; this adaptor links system libandroid.
 */
#include <android/native_activity.h>
#include <android/native_window.h>
#include <stdint.h>
#include "../../NUCLEOS/include/raf_gate.h"
static int gate_selftest(void) {
    raf_gate_input in={RAF_CTRL_ALL,RAF_CTRL_ALL,RAF_CTRL_ALL,0u,0u};
    raf_gate_result r=raf_gate_evaluate(&in);
    if (r.state != RAF_GATE_BLOCKED) return 0;
    in.anchor_verified=1u;
    r=raf_gate_evaluate(&in);
    if(r.state!=RAF_GATE_REVIEW_REQUIRED || r.unknown || r.failing || r.pending) return 0;
    in.known &= ~RAF_CTRL_PRIVACY;
    in.passed &= ~RAF_CTRL_PRIVACY;
    r=raf_gate_evaluate(&in);
    return r.state==RAF_GATE_BLOCKED && r.unknown==RAF_CTRL_PRIVACY;
}
static void draw(ANativeWindow *w) {
    ANativeWindow_Buffer b;
    uint32_t *pixels;
    int x,y;
    int pass;
    if(!w) return;
    if(ANativeWindow_setBuffersGeometry(w,0,0,WINDOW_FORMAT_RGBA_8888)!=0) return;
    if(ANativeWindow_lock(w,&b,0)!=0) return;
    pixels=(uint32_t*)b.bits;
    if(pixels && b.width>0 && b.height>0 && b.stride>=b.width) {
        pass=gate_selftest();
        for(y=0;y<b.height;y++) {
            for(x=0;x<b.width;x++) {
                uint32_t color=0xff182430u;
                if(y<b.height/9) color=pass?0xff318e73u:0xffa53636u;
                if(y>b.height/3 && y<b.height/3+b.height/18)
                    color=0xff80673eu;
                if(y>b.height/2 && y<b.height/2+b.height/18)
                    color=0xff34426bu;
                pixels[y*b.stride+x]=color;
            }
        }
    }
    (void)ANativeWindow_unlockAndPost(w);
}
static void on_window(ANativeActivity *a,ANativeWindow *w) {
    (void)a; draw(w);
}
__attribute__((visibility("default")))
void ANativeActivity_onCreate(ANativeActivity *a,void *saved,size_t count) {
    (void)saved; (void)count;
    if(!a || !a->callbacks) return;
    a->callbacks->onNativeWindowCreated=on_window;
    a->callbacks->onNativeWindowResized=on_window;
    a->callbacks->onNativeWindowRedrawNeeded=on_window;
}
