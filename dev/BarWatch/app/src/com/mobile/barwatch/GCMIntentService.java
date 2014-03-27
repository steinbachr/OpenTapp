package com.mobile.barwatch;

import android.content.Context;
import android.content.Intent;

import com.google.android.gcm.GCMBaseIntentService;
import com.mobile.barwatch.models.Constants;

public class GCMIntentService extends GCMBaseIntentService {
	public GCMIntentService() {
		super(Constants.GOOGLE_SENDER_ID);
	}
	
	@Override
	public void onRegistered(Context context, String regId) {
		//here register the device with the server so we can send it notifications
		System.out.println("IM registered!");
	}
	
	@Override
	public void onUnregistered(Context context, String regId) {
		//here unregister the device with the server so
		System.out.println("IM unregistered!");
	}
	
	@Override
	public void onMessage(Context context, Intent intent) {
		//do stuff with messages received here
		System.out.println("IM messaged!");
	}
	
	@Override
	public void onError(Context context, String errorId) {
		//if we hit an error
		System.out.println("IM errored!");			
	}
	
	@Override
	public boolean onRecoverableError(Context context, String errorId) {
		System.out.println("recoverable error");
		return true;
	}
		
}
