package com.mobile.barwatch.tasks;

import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;

import com.mobile.barwatch.activities.MapScreen;
import com.mobile.barwatch.activities.SplashScreen;

public class SplashWait extends AsyncTask<Void, Integer, Void> {
	private int waitTime;	
	private Context context;
	
	public SplashWait(Context c, int wait) {
		this.context = c;
		this.waitTime = wait;
	}
	
		  
	//The code to be executed in a background thread.  
	@Override  
	protected Void doInBackground(Void... params) {   
	    try { 
	    	synchronized(this) {
	    		this.wait(waitTime);
	    	}
	    } catch (Exception e) {  
            e.printStackTrace();  
        }  
        return null;  
    }  
	  
    //after executing the code in the thread  
	@Override  
	protected void onPostExecute(Void result)  
	{  
		Intent i = new Intent(this.context, MapScreen.class);
		this.context.startActivity(i);			
	}  
}
