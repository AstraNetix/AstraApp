package com.astra.astraapp;

public interface AstraAppResourceMetric {
	public int getCPUThreshold();
	
	public void setCPUThreshold(int cpuThresh);
	
	public int getGPUThreshold();
	
	public void setGPUThreshold(int gpuThresh);
	
	public int getMemoryThreshold();
	
	public void setMemoryThreshold(int memThresh);
	
	public int getDiskThreshold();
	
	public void setDiskThreshold(int diskThresh);
}
