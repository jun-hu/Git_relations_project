#include <iostream>
#include <fstream>
#include <sstream>
#include <map>
#include <list>
#include <string>
#include <algorithm>
#include <functional>
using namespace std;

typedef map<string, list<int> > INDEX;
INDEX m;

int main()
{

	fstream a;
	fstream b;

	a.open("output_cleand2.txt");
	b.open("Commiters.txt");

	// Repositoreis  Stars Followers Follwing
	string re[1000]; // 레포지토리
	string star[1000]; // 스타
	string fo[1000]; // 팔로워
	string fo1[1000]; // 팔로윙

	string id[10000];
	string city[10000];

	string temp;
	string words;
	
	
	int x = 0;

	int num = 0;


	while (true)
	{


		//a >> re[x];
		a >> star[x];
		a >> fo[x];
		a >> fo1[x];
		a >> id[x];
		a >> city[x];

		if (num == 50) // 숫자 변경해야함
		{
			break;

		}

		x = x + 1;

		num = num + 1;

	}

	x = 0;
	num = 0;

	cout << "완료"<<endl;

	//b << "RePositories" << "  " << "Starts" << "  " << "Followers" << "  " << "Following" << "  " << "ID" << "  " << "city" << "  " << endl ;
	b  << "Starts" << " " << "Followers" << " " << "Following" << " " << "ID" << " " << "city"  << endl;

	while (1)
	{

		//b << re[x]  << " " << star[x] <<" " << fo[x] << " "<< fo1[x]<<" " << id[x] << " " << city[x] << " "<< endl;
		b  << star[x] << " " << fo[x] << " " << fo1[x] << " " << id[x] << " " << city[x] << " " << endl;
		//cout << re[x] << star[x] << fo[x] << fo1[x] << id[x] << city[x];
		if (num == 50) // 숫자 변경해야함
		{
			for (int i = 0; i < 10; i++)
			{
				b << endl;
			}

			break;

		}

		x = x + 1;

		num = num + 1;


	}

	////////////////////////////////////
	fstream c;
	fstream d;

	string topic[1000];
	string langle[1000];

	c.open("output_cleand1.txt");
	d.open("Repositories.txt");
	x = 0;
	num = 0;
	
	while (true)
	{

		c >> topic[x];

		if (x==15)//여기 수정해야함
		{
			break;
		}

		x = x + 1;
	}

	x = 0;
	num = 0;

	int ii = 0;


	while (1)
	{

		d << topic[x] << " ";

		if (ii==2)
		{
			d << endl;
			ii = 0;
		}

		ii = ii + 1;
		
		if (num == 15) // 숫자 변경해야함
		{
			for (int i = 0; i < 3; i++)
			{
				d << endl;
			}

			break;

		}

		x = x + 1;

		num = num + 1;


	}

	return 0;
}