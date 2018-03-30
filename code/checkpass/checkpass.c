#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "checkpass.h"
#include "md5.h"

void checkPassword(unsigned char* pwds, int length) {
  unsigned char uname[UBMAX];
  int upos = 0;
  unsigned char c;
  while ((upos < PBMAX) && ((c = getchar()) != '~')) {
    if ((c < 48) || (c > 122)) {
      printf ("Invalid username!");
      exit(1);
    }
    uname[upos++] = c;
  }
  if (c != '~') {
    printf("Username too long!\n");        
    exit(1); // Too long!
  }
  uname[upos] = '~';
  unsigned char password[PBMAX];
  int ppos = 0;
  int sawNumber = 0;
  int sawSpecial = 0;  
  while ((ppos < 512) && ((c = getchar()) != '~')) {
    if ((c < 48) || (c > 122)) {
      printf ("Invalid password!");
      exit(1);
    }    
    if ((c == '0') || (c == '1') || (c == '2') || (c == '3') || (c == '4') || (c == '5') ||
	(c == '6') || (c == '7') || (c == '8') || (c == '9')) {
      sawNumber = 1;
    }
    if ((c == '.') || (c == '*') || (c == '?')) {
      sawSpecial = 1;
    }        
    password[ppos++] = c;
  }
  if (ppos < 16) {
    printf ("Invalid password.\n");
    exit(1);
  }
  if (!(sawNumber && sawSpecial)) {
    printf ("Invalid password.\n");
    exit(1);
  }  
  if (c != '~') {
    printf("Password too long!\n");    
    exit(1); // Too long!
  }
  password[ppos] = 0;
  unsigned char both[PBMAX+UBMAX+1];
  memcpy(uname,both,upos);
  memcpy(password,both+upos+1,ppos);
  memset(both+upos+1+ppos,0,(PBMAX+UBMAX+1)-(upos+1+ppos));
  unsigned char md5buf[PBMAX+UBMAX+1];
  md5(both,2048,md5buf);
  if (strstr((char*)md5buf,(char*)pwds) != 0) {
    printf("Password ok!\n");
    exit(0);
  }
}

int main() {

  unsigned char *buffer = 0;
  long length;
  FILE *f = fopen ("users.pwd", "rb");

  if (f) {
    fseek (f, 0, SEEK_END);
    length = ftell (f);
    fseek (f, 0, SEEK_SET);
    buffer = malloc (length+1);
    if (buffer)
      {
	fread (buffer, 1, length, f);
      }
    fclose (f);
  }

  buffer[length] = 0;
  if (buffer) {
    checkPassword(buffer,length);
    printf("Password incorrect.\n");
    exit(2);
  }
  
}
