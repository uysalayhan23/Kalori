package com.kalori.journal;

import android.app.Activity;
import android.os.Bundle;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebSettings;
import android.webkit.WebResourceRequest;
import android.content.Intent;
import android.net.Uri;

public class MainActivity extends Activity {
    private WebView view;
    private static final String ASSET_ORIGIN = "file:///android_asset/";
    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        view = new WebView(this);
        view.getSettings().setJavaScriptEnabled(true);
        view.getSettings().setDomStorageEnabled(true);
        view.getSettings().setAllowFileAccess(true);
        view.getSettings().setAllowContentAccess(false);
        view.getSettings().setAllowFileAccessFromFileURLs(false);
        view.getSettings().setAllowUniversalAccessFromFileURLs(false);
        view.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest request) {
                Uri uri=request.getUrl();
                if ("file".equals(uri.getScheme()) && uri.toString().startsWith(ASSET_ORIGIN)) return false;
                if ("https".equals(uri.getScheme())) {
                    startActivity(new Intent(Intent.ACTION_VIEW,uri));
                }
                return true;
            }
        });
        setContentView(view);
        view.loadUrl(ASSET_ORIGIN+"index.html");
    }
    @Override public void onBackPressed() {
        if(view != null && view.canGoBack()) view.goBack(); else super.onBackPressed();
    }
    @Override public void onDestroy() {
        if(view != null){view.destroy();view=null;}
        super.onDestroy();
    }
}
