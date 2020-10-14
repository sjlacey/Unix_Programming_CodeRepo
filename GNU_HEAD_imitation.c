/* This program imitates the GNU HEAD function, to the extent as requested
 * by the assignment. It takes a file as input, or in the absence of a
 * file reads from stdin, and performs commands on the text to print:
 * a help/options page, version information, X amount of lines and X
 * amount of odd or even lines.
 *
 * The code works completely.
 * ~ Sean Lacey, 18902826, sean.lacey@ucdconnect.ie
 */
 #include <stdio.h>
 #include <unistd.h>
 #include <stdlib.h>

int readtext(int numoflines, int evenodd, char *filename); //for evenodd 0= neither, 1=odd, 2=even

int main(int argc, char *argv[])
{

  int opt;
  int numoflines;

  while((opt = getopt(argc, argv, "e:o:n:Vh")) != -1)
  {
      switch(opt)
      {
        case 'n':
            numoflines = atoi(optarg);
            readtext(numoflines, 0, argv[3]);
            break;
        case 'V':
            printf("Version 1.0. Author: Sean Lacey, 18902826, sean.lacey@ucdconnect.ie.\n");
            break;
        case 'h':
            printf("Options:\n-n This command, followed by an integer X and the file, will print the first X lines of the file.\n-e This command, followed by an integer X and the file, will print the first X even lines from the text file.\n-o This command, followed by an integer X and the file, will print the first X odd lines from the text file.\n-V This command will print the version info.\nNote: If no file is passed the standard input from the console will be read instead. Use ctrl+D to end the input.\n");
            break;
        case 'o':
            numoflines = atoi(optarg);
            readtext(numoflines, 1, argv[3]);
            break;
        case 'e':
            numoflines = atoi(optarg);
            readtext(numoflines, 2, argv[3]);
            break;
      }
  }
  return 0;
}

int readtext(int numoflines, int evenodd, char *filename)
{
  char list[100][100];
  char burn[100];
  char input[100][100];
  FILE *fptr = fopen(filename, "r");
  int n = 2*(numoflines+1);

  if ((fptr = fopen(filename, "r")) == NULL)
  {
    fptr = stdin;
  }

  for(int i=1; i<n; i++)
  {
    if(evenodd==0) //default case
    {
      fscanf(fptr, "%[^\n]\n", list[i]); //reads text until newline is encountered
    }
    else if(evenodd==1) //odd case
    {
      if(i%2==1)
      {
        fscanf(fptr, "%[^\n]\n", list[i/2]);
      }
      else
      {
        fscanf(fptr, "%[^\n]\n", burn);
      }
    }
    else //even case
    {
      if(i%2==0)
      {
        fscanf(fptr, "%[^\n]\n", list[i/2]);
      }
      else
      {
        fscanf(fptr, "%[^\n]\n", burn);
      }
    }
  }

  if(evenodd==2 || evenodd==0)
  {
    for(int i=1; i<n/2; i++)
    {
      printf("%s\n", list[i]);
    }
  }
  else
  {
    for(int i=0; i<n/2-1; i++)
    {
      printf("%s\n", list[i]);
    }
  }
  fclose(fptr);

}
