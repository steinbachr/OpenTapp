package com.mobile.barwatch.models;

import android.os.Parcel;
import android.os.Parcelable;

public class MenuItem implements Parcelable {
	private int id;
	private String name;
	private double price;
	
	public MenuItem(int id, String name, double price) {
		this.id = id;
		this.name = name;
		this.price = price;
	}
	public MenuItem(Parcel p) {
		this.id = p.readInt();
		this.name = p.readString();		
		this.price = p.readDouble();
	}
	
	public String toString() {		
		return this.name;
	}
	
	/**PARCELABLE STUFF**/
    public static final Parcelable.Creator<MenuItem> CREATOR = new Parcelable.Creator<MenuItem>() {
    	public MenuItem createFromParcel(Parcel in) {
    		return new MenuItem(in);
    	}
		public MenuItem[] newArray(int size) {
			return new MenuItem[size];
		}
    };

    public int describeContents() {
        return 0;
    }

    public void writeToParcel(Parcel out, int flags) {
        out.writeInt(this.id);
        out.writeString(this.name);
        out.writeDouble(this.price);
    }
    /**END PARCELABLE**/
}
