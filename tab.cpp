#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <sstream>
#include "k-nn1.hpp"
#include <fstream>

using namespace std;

int main()
{
    const std::string g_file_name = "good_desc.txt";
    std::ifstream g_file(g_file_name.c_str());
    std::string g_temp;
    vector<vector<double> > a(141);
    for (size_t i=0; i < 141; ++i) {
	   for (std::string temp; g_file && getline(g_file, temp, '\t');) {
	   
	   stringstream ss(temp);
	     double x;
	     ss >> x;
	     a[i].push_back(x);
         if (a[i].size() <= 128) break;
	   }
	 }
	
	
	const std::string m_file_name = "mal_desc.txt";
    std::ifstream m_file(m_file_name.c_str());
    std::string m_temp;
    vector<vector<double> > b(211);
	for (size_t i=0; i < 211; ++i) {
	   for (std::string temp; m_file && getline(m_file, temp, '\t');) {
	     	     stringstream ss(temp);
	     double x;
	     ss >> x;
	     b[i].push_back(x);
	     if (b[i].size() <= 128) break;
	   }
	 }
	
		
	const std::string q_file_name = "query_desc.txt";
    std::ifstream q_file(q_file_name.c_str());
    std::string q_temp;
    vector<vector<double> > p(1384);
    for (size_t i=0; i < 1384; ++i) {
    for (std::string temp; q_file && getline(q_file, temp, '\t');) {
      stringstream ss(temp);
      double x;
      ss >> x;
      p[i].push_back(x);
        if (p[i].size() <= 128) break;
      }
     }

	int k = 20;
	double start = gettimeofday_sec();

	vector<int> ret = k_nn(a,b,p,k);	
	ofstream ofs( "text.txt" );
	for (size_t it = 0; it < ret.size(); ++it) {
		if (ret[it] == 0){
		ofs <<ret[it]<< endl;
	    }else if (ret[it] == 1) {
	    ofs <<ret[it]<< endl;
		}
			
	}
	double end = gettimeofday_sec();
	cout << "Time = " << end - start << " sec." << endl;
	return 0;
}
