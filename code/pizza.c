#include <assert.h>

int main() {
  char a[10];
  char c;
  int i = 0;
  while (i < 10) {
    c = getchar();
    a[i] = c;
    if ((a[i] == 'a') && (a[i-1] == 'z') && (a[i-2] == 'z')
	&& (a[i-3] == 'i') && (a[i-4] == 'p')) {
      assert(0);
    }
    i = i + 1;
  }
  return 0;
}
