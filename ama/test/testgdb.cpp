#include <iostream>
#include <string>

using namespace std;

void gretting(string name)
{
  for(int k=0; k< 10; k++)
    cout << "(Iteration " << k << " )" << " Hello " << name << " (from gretting function)" << endl;
}

int main(int args, char** argv)
{
  string name = "marshal";
  gretting(name);
}
