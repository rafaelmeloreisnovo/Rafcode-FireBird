/* SPDX-License-Identifier: MIT -- original AAR consumer, NOT Firebird server */
package org.rafaelia.firebird.libraryprobe;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.graphics.Typeface;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.File;
import org.firebirdsql.android.embedded.FirebirdConf;

public final class MainActivity extends Activity {
 private TextView result;
 @Override public void onCreate(Bundle state) {
  super.onCreate(state);
  LinearLayout root = new LinearLayout(this);
  root.setOrientation(LinearLayout.VERTICAL);
  root.setPadding(24,30,24,20);
  TextView title = new TextView(this);
  title.setText("Firebird AAR - verificacao da biblioteca");
  title.setTextSize(21);
  title.setTypeface(Typeface.DEFAULT,Typeface.BOLD);
  root.addView(title);
  result = new TextView(this);
  result.setTextSize(16);
  result.setPadding(0,20,0,20);
  root.addView(result);
  Button test = new Button(this);
  test.setText("EXECUTAR TESTE");
  test.setOnClickListener(new View.OnClickListener() {
   @Override public void onClick(View v) { probe(); }
  });
  root.addView(test);
  setContentView(root);
  probe();
 }
 private void probe() {
  String abi = Build.SUPPORTED_ABIS.length>0 ? Build.SUPPORTED_ABIS[0] : "UNKNOWN";
  boolean aar = FirebirdConf.class.getName().equals("org.firebirdsql.android.embedded.FirebirdConf");
  File client = new File(getApplicationInfo().nativeLibraryDir,"libfbclient.so");
  boolean packed = client.isFile();
  StringBuilder s = new StringBuilder();
  s.append("Android ABI: ").append(abi).append('\n');
  s.append("Android API: ").append(Build.VERSION.SDK_INT).append('\n');
  s.append("AAR FirebirdConf: ").append(aar?"PASS":"BLOCKED").append('\n');
  s.append("Native libfbclient.so: ").append(packed?"PRESENT":"ABSENT").append('\n');
  s.append("Motor Firebird SQL: NOT_VALIDATED\n");
  s.append("Transacoes e banco: NOT_RUN\n");
  if (packed) {
   try {
    System.loadLibrary("fbclient");
    s.append("Client loader: PASS (NOT SQL)\n");
   } catch (UnsatisfiedLinkError ex) {s.append("Client loader: BLOCKED\n");}
  }
  s.append("APK de TESTE DA BIBLIOTECA, nao servidor.\n");
  result.setText(s.toString());
 }
}
