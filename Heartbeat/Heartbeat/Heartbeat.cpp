#include<iostream>
#include<windows.h>

const int duration = 3;
unsigned short data[64008 * duration];
HANDLE hCom, hFile;
DWORD nin, nout;

int main(int argc, LPTSTR argv[])
{
	hCom = CreateFile("\\\\.\\COM5", (GENERIC_READ | GENERIC_WRITE), (FILE_SHARE_READ | FILE_SHARE_WRITE), NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	hFile = CreateFile("data.bin", (GENERIC_READ | GENERIC_WRITE), (FILE_SHARE_READ | FILE_SHARE_WRITE), NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);

	if (hCom == INVALID_HANDLE_VALUE)
	{
		std::cout << "Device not found" << std::endl;
		return 1;
	}

	if (hFile == INVALID_HANDLE_VALUE)
	{
		std::cout << "Error in file creation" << std::endl;
		return 2;
	}

	ReadFile(hCom, &data, 64008 * duration, &nin, NULL);
	WriteFile(hFile, &data, 64008 * duration, &nout, NULL);
	CloseHandle(hCom);
	CloseHandle(hFile);

	return 0;
}
