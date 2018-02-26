package com.astra.astraapp;

public interface AstraIdentity {
	public String getBOINCUserName();
	
	public void setBOINCUserName(String userName);
	
	public String getEncryptBOINCPassword();
	
	public void setEncryptedBOICPassword(String encryptedPassword);
}
