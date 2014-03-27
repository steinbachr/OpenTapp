package com.mobile.barwatch.models;

public class Constants {
	public static int COORDINATE_MULT_CONSTANT = 1000000;
	/*SERVICE URLS*/
	public static final String BAR_SERVICE_URL = "http://slutty-ninja.dnsdynamic.com:8000/drinkup/service/get-bars";
	public static final String COUPON_SERVICE_URL = "http://slutty-ninja.dnsdynamic.com:8000/drinkup/service/get-coupon"; 
	public static final String REGISTER_PHONE_URL = "http://slutty-ninja.dnsdynamic.com:8000/drinkup/service/register-mobile";
	public static final String REDEEM_COUPON_URL  = "http://slutty-ninja.dnsdynamic.com:8000/drinkup/service/redeem-coupon";
	
	/*API KEYS*/
	public static final String GOOGLE_API_KEY = "AIzaSyCz1c_IrgTCVFRqtc4UwYLvKi9Tb4YCBws";
	public static final String GOOGLE_MAPS_KEY = "AIzaSyDEeB2kC5Luk700KV5pKEgRpf39n4iIV-Y";
	public static final String GOOGLE_SENDER_ID = "672171919192";
	
	/*INTENT EXTRAS KEYS*/
	public static final String BAR_EXTRA = "bar";
	public static final String COUPON_EXTRA = "coupon";
	public static final String REFRESHER_EXTRA = "refresher";
	public static final String MENU_EXTRA = "menu";
	
	/*GLOBAL VALUES*/
	public static final int SDK_VERSION = 0;
	public static final String SHARED_PREFS = "SharedPrefsFile";	
	
	/*ENUMS*/
	public enum CouponType { 
		COVER ("Cover"), 
		DRINKS ("Drinks");
		
		private String key;
		CouponType(String key) {
			this.key = key;
		}
		
		public String key() {
			return this.key;
		}
		
		public static CouponType fromKey(String key) {
			for (CouponType ct : CouponType.values()) {
				if (ct.key().equals(key)) {
					return ct;
				}
			}
			
			return null;	//should never get here
		}
	}
	public enum AlcoholType { 
		SHOT ("Shot"),
		MIXED_DRINK ("Mixed Drink"), 
		BEER ("Beer"), 
		NONE("");
		
		private String key;
		AlcoholType(String key) {
			this.key = key;
		}
		
		public String key() {
			return this.key;
		}
		
		public static AlcoholType fromKey(String key) {
			for (AlcoholType ct : AlcoholType.values()) {
				if (ct.key().equals(key)) {
					return ct;
				}
			}
			
			return NONE;
		}
	}
}
