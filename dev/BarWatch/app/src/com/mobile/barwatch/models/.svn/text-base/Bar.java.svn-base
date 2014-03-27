package com.mobile.barwatch.models;

import java.util.*;
import java.util.concurrent.ExecutionException;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import com.mobile.barwatch.tasks.CallWebService;

import android.os.Parcel;
import android.os.Parcelable;


public class Bar implements Parcelable {
	private int id;
	private String name;
	private double latitude;
	private double longitude;	
	private ArrayList<Coupon> coupons = new ArrayList<Coupon>();
	private Menu menu;
	private String address;
	
	public Bar(int id, String name, double latitude, double longitude, ArrayList<Coupon> coupons, Menu menu, String address) {
		this.id = id;
		this.name = name;
		this.latitude = latitude;
		this.longitude = longitude;
		this.coupons = coupons;
		this.menu = menu;
		this.address = address;
	}
	private Bar(Parcel p) {		
		this.id = p.readInt();
		this.name = p.readString();		
		this.latitude = p.readDouble();
		this.longitude = p.readDouble();
		p.readTypedList(coupons, Coupon.CREATOR);		
		this.menu = p.readParcelable(Menu.class.getClassLoader());
		this.address = p.readString();
	}
	
	public int id() {
		return this.id;
	}
	public String name() {
		return this.name;
	}
	public double latitude() {
		return this.latitude;
	}
	public double longitude() {
		return this.longitude;
	}
	public ArrayList<Coupon> coupons() {
		return this.coupons;
	}
	public Menu menu() {
		return this.menu;
	}
	public String address() {
		return this.address;
	}
	
	/**INSTANCE METHODS**/
	public long coordinateForMap(double coord) {
		return java.lang.Math.round(coord * Constants.COORDINATE_MULT_CONSTANT);
	}
	
	public String toString() {
		return this.name;
	}
	/**END INSTANCE METHODS**/
	
	/**PARCELABLE STUFF**/
    public static final Parcelable.Creator<Bar> CREATOR = new Parcelable.Creator<Bar>() {
    	public Bar createFromParcel(Parcel in) {
    		return new Bar(in);
    	}
		public Bar[] newArray(int size) {
			return new Bar[size];
		}
    };

    public int describeContents() {
        return 0;
    }

    public void writeToParcel(Parcel out, int flags) {
        out.writeInt(this.id());
        out.writeString(this.name());
        out.writeDouble(this.latitude());
        out.writeDouble(this.longitude()); 
        out.writeTypedList(this.coupons());         
    	out.writeParcelable(this.menu(), 0);        
        out.writeString(this.address());
    }
    /**END PARCELABLE**/
    
    /**STATIC METHODS**/	
	public static ArrayList<Bar> getBarsFromDb() throws InterruptedException,ExecutionException {
		return fromJson(new CallWebService().execute(Constants.BAR_SERVICE_URL).get());
	}
	
	private static ArrayList<Bar> fromJson(String json) {		
		ArrayList<Bar> bars = new ArrayList<Bar>();
						
		Gson gson = new GsonBuilder().disableHtmlEscaping().create();        
        try  
        {         	
            bars = new ArrayList<Bar>(Arrays.asList(gson.fromJson(json, Bar[].class)));            
        }  
        catch(Exception e)  
        {  
            e.printStackTrace();  
        }        
		return bars;
	}
	/**END STATIC**/
}
