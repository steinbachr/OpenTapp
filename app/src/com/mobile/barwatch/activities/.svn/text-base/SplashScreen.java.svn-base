package com.mobile.barwatch.activities;

import android.app.Activity;
import android.os.Bundle;

import com.google.android.gcm.GCMRegistrar;

import com.google.android.gms.common.*;

import com.mobile.barwatch.R;
import com.mobile.barwatch.tasks.*;
import com.mobile.barwatch.R.layout;
import com.mobile.barwatch.models.Constants;

public class SplashScreen extends Activity {
	private static final int WAIT_TIME = 2000;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {    	   	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.splash_screen);   
        
        int playServicesStatus = GooglePlayServicesUtil.isGooglePlayServicesAvailable(this);
        if (!(playServicesStatus == ConnectionResult.SUCCESS)) {
        	GooglePlayServicesUtil.getErrorDialog(playServicesStatus, this, 0);
        }
        
        GCMRegistrar.checkDevice(this);
        GCMRegistrar.checkManifest(this);
        final String regId = GCMRegistrar.getRegistrationId(this);        

        if(regId.equals("")) {
        	GCMRegistrar.register(this.getApplicationContext(), Constants.GOOGLE_SENDER_ID);
        } else {
        	System.out.println("This device already registered");
        }
                
        new SplashWait(this, WAIT_TIME).execute();        
    }
    
	public void onPause() {
		super.onPause();
	}
	
	public void onDestroy() {
		super.onDestroy();
	}
	
	public void onStop() {
		super.onStop();
	}	
	
	
}

