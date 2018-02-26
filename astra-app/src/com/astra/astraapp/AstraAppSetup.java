package com.astra.astraapp;

public interface AstraAppSetup {

	public enum Major_Platform {
		WINDOWS,
		OSX,
		LINUX,
		iOS,
		ANDROID
	}
	
	public Major_Platform getPlatform();
	
	public void installBOINC(Major_Platform platform, String location);
	
	public void setBOINCCredentials(AstraIdentity identity);
	
	public AstraIdentity getBOICCredentials();
}
