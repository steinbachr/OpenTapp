package com.mobile.barwatch.models;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.mobile.barwatch.tasks.CallWebService;

import android.content.Context;
import android.content.SharedPreferences;

public class MobileUser {
	private String PHONE_ID = "PHONE_ID";
	private Context context;
	private int phoneId;
	
	public MobileUser(Context c) {
		this.context = c;
		this.phoneId = registerPhone();		
	}
	
	public int phoneId() {
		return this.phoneId;
	}
	
	//parse the json string returned by the register-phone service in order to get the phones id
	private int parseJson(String jsonString) {		
		int phoneId;
		try {
			JSONObject couponDetails = new JSONObject(jsonString);		
			phoneId = couponDetails.getInt("id");			
		} catch (JSONException e) {
			phoneId = -1;
		}		
		
		return phoneId;
	}
	
    private int registerPhone() {
    	SharedPreferences settings = context.getSharedPreferences(Constants.SHARED_PREFS, 0);
    	this.phoneId = settings.getInt(PHONE_ID, -1);
    	if (this.phoneId < 0) {
    		SharedPreferences.Editor editor = settings.edit();
        	try {
        		String json = new CallWebService().execute(Constants.REGISTER_PHONE_URL).get();
        		this.phoneId = this.parseJson(json);
        		
        		editor.putInt(PHONE_ID, this.phoneId);
        		editor.commit();
        	} catch(Exception e) {
        		//TODO: handle this
        	}    
    	} 
    	
    	return this.phoneId;
    }
    
    public String redeemCoupon(int couponId) {
    	try {    		
    		String redemptionFlash = new CallWebService().execute(Constants.REDEEM_COUPON_URL+"?coupon_id="+couponId+"&phone_id="+this.phoneId).get();    		
    		return redemptionFlash;
    	} catch (Exception e) {
    		return "Oops, something went wrong when we tried to redeem the coupon for you";
    	}
    }
}
