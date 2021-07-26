/*
 * RCS info
 * $Author: steves $
 * $Locker:  $
 * $Date: 2018/10/17 20:44:31 $
 * $Id: awips2nbtcp.c,v 1.2 2018/10/17 20:44:31 steves Exp $
 * $Revision: 1.2 $
 * $State: Exp $
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

/***************************************************************************************

   Converts AWIPS RPS list format to nbtcp RPS list format.  

   AWIPS RPS list is assumed to be in the following format:

      - first line lists file name, when it was created and how many products
      - second, third and fourth lines list the contents of each token in the record
      - the fifth line lists the record format.  

   Here is an examplei of the first 5 lines of the file:

      RPS List KCRI.storm.VCP12.rps created        2013:04:18:21:00:00 ... 81 products
       An RPS list contains the fields: Prod-Name, Mnemonic, Prod-Code
       Number of Data Levels, Resolution, Layer Code, Elevation, Contour Interval,
       Priority, Req Interval, Map, Lower Layer, Upper Layer, multCut, endHour, timeSpan
       The record format is: '%-39s  %-3s%4d%4d%6d %c%6d%7d%2d%2d%c%3d%3d %c%7d%7d'

   Here is an example of a record:
      Reflectivity (Z)                         Z    19  16   100 -  8227     -1 0 1N -1 -1 N     -1      0

   An nbtcp RPS list has the following format:

      count  code  mnemonic description parameters.

   It is read in by nbtcp using the following format:

      %4s %5s %5s %50c %s %s %s %s %s %s

*****************************************************************************************/

#define MIN_EXP_ITEMS           13
#define INP_EXP_ITEMS		15
#define MAX_INP_NAME		39
#define ALL_ELEVATIONS		16384

int main( int argc, char *argv[] ){

   char outfile[256];
   char buf[256];
   FILE *out_fd = NULL;
   FILE *in_fd = NULL;
   int items = 0;

   /* Input variables. */
   char name[64], mnem[8], lcode, multcut, map;
   int code, levels, res, elev, cont_int, pri, req_int, llay;
   int ulay, endhour, timespan;

   /* Output variables. */
   char param1[8], param2[28], param3[8], param4[8], param5[8], param6[8];
   int cnt;

   /* Name of file should be argv[1]. */
   fprintf( stderr, "AWIPS RPS List File: %s\n", argv[1] );

   /* Create a nbtcp compatible RPS list file with the same name, 
      but with .nbtcp extension. */
   memset( &outfile[0], 0, 256 );
   sprintf( &outfile[0], "./%s.nbtcp", argv[1] );

   /* Attempt to create this file with write permission. */
   out_fd = fopen( outfile, "w" );
   if( out_fd == NULL ){

      fprintf( stderr, "Failed in creating nbtcp RPS file: %s (errno: %d)\n", 
               outfile, errno );
      exit(0);

   }

   /* Open the input file for reading. */
   in_fd = fopen( argv[1], "r" );
   if( in_fd == NULL ){

      fprintf( stderr, "failed in opening AWIPS RPS file: %s (errno: %d)\n",
               argv[1], errno );
      exit(0);

   }

   /* Read the input file and write the output file. */

   /* Skip the first part of the file .... */
   while( fgets( buf, sizeof(buf), in_fd ) != NULL ){

      if( strstr( buf, "The record format is:" ) != NULL ){

         fprintf( stderr, "Start Processing RPS record .....\n" );
         break;

      }

   }

   /* Process the records. */
   cnt = 0;
   while( fgets( buf, sizeof(buf), in_fd ) != NULL ){

      fprintf( stderr, "Input Record: %s", buf );

      /* The first 39 characters we assign to the name. */
      if( strlen( buf ) <= MAX_INP_NAME ){

         fprintf( stderr, "Input record Error.  Record too short.\n" );
         exit(0);

      }

      /* Copy the name. */
      memcpy( &name[0], buf, MAX_INP_NAME );
      name[MAX_INP_NAME] = '\0';

      /* Process the rest of the record. */
      items = sscanf( &buf[MAX_INP_NAME], "%3s%4d%4d%6d %c%6d%7d%2d%2d%c%3d%3d %c%7d%7d\n",
                      &mnem[0], &code, &levels, &res, &lcode, &elev, 
                      &cont_int, &pri, &req_int, &map, &llay, &ulay, &multcut, 
                      &endhour, &timespan );
  
      if( items == EOF ){

         fprintf( stderr, "Unexpected Error (errno: %d).  Items Read: %d\n", errno, items );
         break;

      }
      else if( (items != INP_EXP_ITEMS)
                      &&
               (items != MIN_EXP_ITEMS) ){

         fprintf( stderr, "Unexpected Number Items Read: %d\n", items );
         break;

      }

      cnt++;

      /* Initialize parameters to unused. */
      sprintf( &param1[0], "UNU" );
      sprintf( &param2[0], "UNU" );
      sprintf( &param3[0], "UNU" );
      sprintf( &param4[0], "UNU" );
      sprintf( &param5[0], "UNU" );
      sprintf( &param6[0], "UNU" );

      /* Based of product code or other criteria, set parameters. */

      /* Is an elevation angle defined? */
      if( elev != -1 ){

         /* As is ??? */ 
         if( multcut =='N' )
            sprintf( &param3[0], "%6d", elev );

         else
            sprintf( &param3[0], "%6d", ALL_ELEVATIONS+elev ); 

      }

      /* Does the product have time span/end hour defined? */
      if( items == INP_EXP_ITEMS ){

         if( (code == 31) /* USP */
                   ||
             (code == 150) /* USW */
                   ||
             (code == 151) /* USD */
                   ||
             (code == 173) /* DUA */ ){

            sprintf( &param1[0], "%6d", endhour );
            sprintf( &param2[0], "%6d", timespan );

         }

      }

      /* Lower and upper layer defined ??? */
      if( (code == 137 ) /* ULR  */ ){

         sprintf( &param1[0], "%6d", llay );
         sprintf( &param2[0], "%6d", ulay );

      }

      fprintf( out_fd, "%3d   %4d   %-3s  %-50s  %6s     %6s     %6s     %6s     %6s     %6s\n",
               cnt, code, &mnem[0], &name[0], &param1[0], &param2[0], &param3[0],
               &param4[0], &param5[0], &param6[0] );
    
   } 
   
   fclose( in_fd );
   fclose( out_fd );

   return 0;

}

