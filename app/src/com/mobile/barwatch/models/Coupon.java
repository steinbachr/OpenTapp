package com.mobile.barwatch.models;


import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.mobile.barwatch.tasks.CallWebService;

import android.os.Parcel;
import android.os.Parcelable;

public class Coupon implements Parcelable {
	private int id;	
	private String couponType;
	private String alcoholType;
	private String alcoholSpecifics;
	private double originalPrice;	
	private double newPrice;		
	private int numRemaining;
	private int timeRemaining;
	
	public Coupon(int id, String ct, String at, String as, double op, double np, int nRemaining, int tRemaining) {
		this.id = id;
		this.couponType = ct;
		this.alcoholType = at;
		this.alcoholSpecifics = as;
		this.originalPrice = op;	
		this.newPrice = np; 
		this.numRemaining = nRemaining;
		this.timeRemaining = tRemaining;
	}
	private Coupon(Parcel p) {
		this.id = p.readInt();
		this.couponType = p.readString();	
		this.alcoholType = p.readString();
		this.alcoholSpecifics = p.readString();
		this.originalPrice = p.readDouble();	
		this.newPrice = p.readDouble(); 
		this.numRemaining = p.readInt();
		this.timeRemaining = p.readInt();		
	}
	
	/***GETTERS***/
	public int id() {
		return this.id;
	}
	public String couponType() {
		return this.couponType;
	}
	public String alcoholType() {
		return this.alcoholType;
	}
	public String alcoholSpecifics() {
		return this.alcoholSpecifics;
	}
	public double originalPrice() {
		return this.originalPrice;		
	}
	public double newPrice() {
		return this.newPrice;
	}
	public int numRemaining() {
		return this.numRemaining;
	}
	public int timeRemaining() {
		return this.timeRemaining;
	}
	
	/**INSTANCE METHODS**/	
	public String toString() {
		return this.couponType + " coupon";
	}
	/**@return true if coupon can be redeemed, false o/w**/
	public boolean useCoupon() {
		if (this.numRemaining <= 0 || this.timeRemaining < 0) {
			return false;
		}
		else {
			this.numRemaining--;
			return true;
		}
	}
	/**PARCELABLE STUFF**/
    public static final Parcelable.Creator<Coupon> CREATOR = new Parcelable.Creator<Coupon>() {
    	public Coupon createFromParcel(Parcel in) {
    		return new Coupon(in);
    	}
		public Coupon[] newArray(int size) {
			return new Coupon[size];
		}
    };

    public int describeContents() {
        return 0;
    }

    public void writeToParcel(Parcel out, int flags) {
        out.writeInt(this.id());
        out.writeString(this.couponType);
        out.writeString(this.alcoholType);
        out.writeString(this.alcoholSpecifics);
        out.writeDouble(this.originalPrice);
        out.writeDouble(this.newPrice);        
        out.writeInt(this.numRemaining());
        out.writeInt(this.timeRemaining());        
    }
    /**END PARCELABLE**/
    
    /**STATIC METHODS**/	
	public Coupon getCouponFromDb() throws Exception {
		try {			
			return fromJson(new CallWebService().execute(Constants.COUPON_SERVICE_URL+"?id="+this.id).get());
		} catch (Exception e) {
			throw new Exception("unable to get coupon data from db");
		}
	}
	
	public static Coupon fromJson(String json) {		
		Coupon coupon = null;

		Gson gson = new GsonBuilder().disableHtmlEscaping().create();        
        try  
        {          	
            coupon = gson.fromJson(json, Coupon.class);           
        }  
        catch(Exception e)  
        {  
            e.printStackTrace();  
        }
                
        
        return coupon;
	}
	/**END STATIC**/
}
