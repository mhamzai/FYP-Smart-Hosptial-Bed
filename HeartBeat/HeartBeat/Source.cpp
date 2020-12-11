#include<iostream>
#include<windows.h>
#include<fstream>
#include <sstream>

using namespace std;
int main(int argc, LPTSTR argv[])
{
	//unsigned short data[64008];
	unsigned short data[(32004*3)];
	HANDLE hCom, hFile;
	DWORD nin, nout;
	// \\\\.\\ 
	const wchar_t* pcCommPort = TEXT("\\\\.\\COM3");
	const wchar_t* File = TEXT("data.bin");
	ofstream myfile;
	myfile.open("data.txt");
	hCom = CreateFile(pcCommPort, (GENERIC_READ | GENERIC_WRITE), (FILE_SHARE_READ | FILE_SHARE_WRITE), NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	hFile = CreateFile(File, (GENERIC_READ | GENERIC_WRITE), (FILE_SHARE_READ | FILE_SHARE_WRITE), NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL);

	if (hCom == INVALID_HANDLE_VALUE)
	{
		cout << "Device not found" << endl;
		return 1;
	}
	if (!myfile.is_open())//(hFile == INVALID_HANDLE_VALUE)
	{
		cout << "Error in file creation" << endl;
		return 2;
	}
	std::ostringstream os;

		ReadFile(hCom, &data, (64008*3), &nin, NULL);
		
		for (int i : data) {
			os << i;
		}

	std::string str(os.str());
	std::cout << str;
	myfile << str;
	//dat = str.c_str();
	WriteFile(hFile, &data, (64008*3), &nout, NULL);
	CloseHandle(hCom);
	CloseHandle(hFile);
	myfile.close();
	return 0;
}