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


vector<int> k_nn(const vector<vector<double> >& a, const vector<vector<double> >& b, const vector<vector<double> >& p, int k){
  vector<int> result_class;
  double step = (double)k/3;
  for (size_t ik = 0; ik < p.size(); ++ik) {
	if (k > a.size() + b.size()){
		throw "k is too big ";
	}
    vector<pair<double, int> > dists;
    dists.resize(a.size() + b.size());
    for (size_t i = 0; i < a.size(); ++i) {
		dists[i] = make_pair(dists_get(a[i], p[ik]), 0);
	}
	
    for (size_t i=0; i < b.size(); ++i){
	dists[i+a.size()] = make_pair(dists_get(b[i],p[ik]),1);
    }
	
    sort(dists.begin(),dists.end());
	
    int a_num = 0;
    int b_num = 0;
	
    for (size_t i = 0; i < k; ++i){
	if(dists[i].second == 0){
		++a_num;
	}else if (dists[i].second == 1){
		++b_num;
	}else{
		throw "what are you doing?";
	}			
    }
    //a is good, b is mal
    if(a_num-2 >= b_num) {
	result_class.push_back(0);
    }else{
        if(b_num > k-step*1){
             result_class.push_back(3);
        }
        if(b_num > k-step*2) {
             result_class.push_back(2);
        }
	result_class.push_back(1);
   }
 }
  return result_class;
}

double gettimeofday_sec(){
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + (double)tv.tv_usec*1e-6;
}

int nn(const vector<vector<double> >& a, const vector<vector<double> >& b,const vector<vector<double> >& e, const vector<vector<double> >& p){
	
  std::vector<double> a_average;
  a_average.resize(a[0].size());
  for (size_t i = 0; i < a[0].size(); ++i) {
    for(size_t j = 0; j < a.size(); ++j) {
      a_average[i] += a[j][i];
    }
  }
	
  for (size_t i=0; i < a_average.size(); ++i) {
	double tmp_a = (double)a_average[i]/a.size();
	a_average[i] = tmp_a;
  } 
	
  std::vector<double> b_average;
  b_average.resize(b[0].size());
  for (size_t i = 0; i < b[0].size(); ++i) {
	for(size_t j = 0; j < b.size(); ++j) {
          b_average[i] += b[j][i];
	}
   }
		
  for (size_t i=0; i < b_average.size(); ++i) {
	double tmp_b = (double)b_average[i]/b.size();
	b_average[i] = tmp_b;
  }

  std::vector<double> e_average;
  e_average.resize(e[0].size());
  for (size_t i = 0; i < e[0].size(); ++i) {
        for(size_t j = 0; j < e.size(); ++j) {
          e_average[i] += e[j][i];
        }
   }

  for (size_t i=0; i < e_average.size(); ++i) {
        double tmp_e = (double)e_average[i]/e.size();
        e_average[i] = tmp_e;
  } 

  double a_res;
  double b_res;
  double e_res;
  for (size_t ik = 0; ik < p.size(); ++ik) {
    a_res += dists_get(a_average, p[ik]);
    b_res += dists_get(b_average, p[ik]);
    e_res += dists_get(e_average, p[ik]);
  }

  if(a_res > b_res){
    if(b_res > e_res){
	return 2;
    }else{
	return 1;
    }
  }else{
    if(a_res > e_res){
	return 2;
    }else{
        return 0;
    }
  }			
}
