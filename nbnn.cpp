#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <time.h>
#include <sys/time.h>

using namespace std;

double dists_get(const vector<double>& x,const vector<double>& y) {
	if(x.size() != y.size()){
		throw "x and y are completely different dude ";
	}
	double ret = 0;
	for (size_t i = 0;i < x.size(); ++i) {
		double diff = x[i]-y[i];
		ret += diff*diff;
	}
	return ret;
}


vector<pair<double, int> > nbnn(const vector<vector<double> >& a, const vector<vector<double> >& b, const vector<vector<double> >& p, int k){
  vector<int> result_class;

  for (size_t ik = 0; ik < p.size(); ++ik) {
	
	if (k > a.size() + b.size()){
		throw "k is too big ";
	}
	
    vector<pair<double, int> > dists;
    dists.resize(a.size() + b.size());
    vector<pair<double, int> > result_dists;

    for (size_t i = 0; i < a.size(); ++i) {
		dists[i] = make_pair(dists_get(a[i], p[ik]), 0);
	}
	
	for (size_t i=0; i < b.size(); ++i){
		dists[i+a.size()] = make_pair(dists_get(b[i],p[ik]),1);
	}
	
	sort(dists.begin(),dists.end());
	
	/*
 *  * 	for(size_t i=0; i < dists.size(); ++i){
 *   * 			cout << i << ":dists_get=" << dists[i].first <<  ", a or b" << dists[i].second << endl;
 *    * 				}
 *     * 					*/
	int a_num = 0;
	int b_num = 0;
	
	for (size_t i = 0; i < k; ++i){
		if(dists[i].second == 0){
			result_dists = make_pair(dists[i].first, dists[i].second);
		}else { continue;
                }
	}
        
        for (size_t i = 0; i < k; ++i){
                if(dists[i].second == 1){
                        result_dists = make_pair(dists[i].first, dists[i].second);
                }else { continue;
                }
        }
			
	}
	/*
 *  * 	cout << "a_num=" << a_num <<"/ b_num=" << b_num << endl;
 *   * 		*/
  }
  return result_dists;
}

double gettimeofday_sec(){
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + (double)tv.tv_usec*1e-6;
}
