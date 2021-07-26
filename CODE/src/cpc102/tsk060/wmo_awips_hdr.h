/********************************************************************************
 * Internal include file for nbtcp (narrowband TCP ORPG client)
 * Configuration changes made be made to arguments section
 ********************************************************************************/

/*
 * RCS info
 * $Author: steves $
 * $Locker:  $
 * $Date: 2018/03/30 19:51:50 $
 * $Id: wmo_awips_hdr.h,v 1.1 2018/03/30 19:51:50 steves Exp $
 * $Revision: 1.1 $
 * $State: Exp $
 */

#ifndef WMO_AWIPS_HDR_H
#define WMO_AWIPS_HDR_H

typedef struct radar_sites {

   char *radar;
   char *distribution;

} Radar_sites_t;

static Radar_sites_t Radar_sites[] = {
                              { "PACG (Sitka/Biorka Island)", "88" },
                              { "PAEC (Nome)", "88" },
                              { "PAIH (Middleton Island)", "88" },
                              { "PAKC (King Salmon)", "89" },
                              { "PAHG (Kenai)", "89" },
                              { "PAPD (Fairbanks/Pedro Dome)", "89" },
                              { "PABC (Bethel)", "89" },
                              { "KMOB (Mobile)", "84" },
                              { "KMXX (Maxwell AFB)", "84" },
                              { "KHTX (Huntsville)", "84" },
                              { "KEOX (Fort Rucker)", "84" },
                              { "KBMX (Birmingham)", "84" },
                              { "KLZK (Little Rock)", "84" },
                              { "KSRX (Fort Smith)", "84" },
                              { "KYUX (Yuma)", "85" },
                              { "KEMX (Tucson)", "85" },
                              { "KIWA (Phoenix)", "85" },
                              { "KFSX (Flagstaff)", "85" },
                              { "KVBX (Vandenberg AFB)", "86" },
                              { "KSOX (Santa Ana Mountains)", "86" },
                              { "KHNX (San Joaquin Valley)", "86" },
                              { "KMUX (San Francisco)", "86" },
                              { "KNKX (San Diego)", "86" },
                              { "KDAX (Sacramento)", "86" },
                              { "KVTX (Los Angeles)", "86" },
                              { "KBHX (Eureka)", "86" },
                              { "KEYX (Edwards AFB)", "86" },
                              { "KBBX (Beale AFB)", "86" },
                              { "KPUX (Pueblo)", "85" },
                              { "KGJX (Grand Junction)", "85" },
                              { "KFTG (Denver)", "85" },
                              { "KDOX (Dover AFB)", "81" },
                              { "KTBW (Tampa)", "82" },
                              { "KTLH (Tallahassee)", "82" },
                              { "KAMX (Miami)", "82" },
                              { "KMLB (Melbourne)", "82" },
                              { "KBYX (Key West)", "82" },
                              { "KJAX (Jacksonville)", "82" },
                              { "KEVX (Eglin AFB)", "82" },
                              { "KJGX (Robins AFB)", "82" },
                              { "KVAX (Moody AFB)", "82" },
                              { "KFFC (Atlanta)", "82" },
                              { "PGUA (Andersen AFB)", "00" },
                              { "PHWA (South Shore)", "80" },
                              { "PHMO (Molokai)", "80" },
                              { "PHKM (Kohala)", "80" },
                              { "PHKI (Kauai)", "80" },
                              { "KDMX (Des Moines)", "83" },
                              { "KDVN (Davenport)", "83" },
                              { "KSFX (Pocatello/Idaho Falls)", "85" },
                              { "KCBX (Boise)", "85" },
                              { "KILX (Lincoln)", "83" },
                              { "KLOT (Chicago)", "83" },
                              { "KIWX (North Webster)", "83" },
                              { "KIND (Indianapolis)", "83" },
                              { "KVWX (Evansville)", "83" },
                              { "KICT (Wichita)", "83" },
                              { "KTWX (Topeka)", "83" },
                              { "KGLD (Goodland)", "83" },
                              { "KDDC (Dodge City)", "83" },
                              { "KPAH (Paducah)", "83" },
                              { "KLVX (Louisville)", "83" },
                              { "KJKL (Jackson)", "83" },
                              { "KHPX (Fort Campbell)", "83" },
                              { "KSHV (Shreveport)", "84" },
                              { "KLIX (New Orleans)", "84" },
                              { "KLCH (Lake Charles)", "84" },
                              { "KPOE (Fort Polk)", "84" },
                              { "KBOX (Boston)", "81" },
                              { "KGYX (Portland)", "81" },
                              { "KCBW (Loring AFB)", "81" },
                              { "KMQT (Marquette)", "83" },
                              { "KGRR (Grand Rapids)", "83" },
                              { "KAPX (Gaylord)", "83" },
                              { "KDTX (Detroit/Pontiac)", "83" },
                              { "KMPX (Minneapolis/St. Paul)", "83" },
                              { "KDLH (Duluth)", "83" },
                              { "KLSX (St. Louis)", "83" },
                              { "KSGF (Springfield)", "83" },
                              { "KEAX (Kansas City)", "83" },
                              { "KGWX (Columbus AFB)", "84" },
                              { "KDGX (Brandon/Jackson)", "84" },
                              { "KMSX (Missoula)", "85" },
                              { "KTFX (Great Falls)", "85" },
                              { "KGGW (Glasgow)", "85" },
                              { "KBLX (Billings)", "85" },
                              { "KLTX (Wilmington)", "82" },
                              { "KRAX (Raleigh/Durham)", "82" },
                              { "KMHX (Morehead City)", "82" },
                              { "KMBX (Minot AFB)", "83" },
                              { "KMVX (Grand Forks (Mayville))", "83" },
                              { "KBIS (Bismarck)", "83" },
                              { "KOAX (Omaha)", "83" },
                              { "KLNX (North Platte)", "83" },
                              { "KUEX (Grand Island/Hastings)", "83" },
                              { "KHDX (Holloman AFB)", "85" },
                              { "KFDX (Cannon AFB)", "85" },
                              { "KABX (Albuquerque)", "85" },
                              { "KRGX (Reno)", "85" },
                              { "KESX (Las Vegas)", "85" },
                              { "KLRX (Elko)", "85" },
                              { "KOKX (New York City)", "81" },
                              { "KTYX (Montague)", "81" },
                              { "KBUF (Buffalo)", "81" },
                              { "KBGM (Binghamton)", "81" },
                              { "KENX (Albany)", "81" },
                              { "KILN (Wilmington)", "81" },
                              { "KCLE (Cleveland)", "81" },
                              { "KVNX (Vance AFB)", "84" },
                              { "KINX (Tulsa)", "84" },
                              { "KTLX (Oklahoma City)", "84" },
                              { "NOP3 (ROC)", "84" },
                              { "NOP4 (ROC)", "84" },
                              { "ROP3 (ROC)", "84" },
                              { "ROP4 (ROC)", "84" },
                              { "FOP1 (ROC)", "84" },
                              { "DOP1 (ROC)", "84" },
                              { "DAN1 (ROC)", "84" },
                              { "KFDR (Frederick)", "84" },
                              { "KOUN (NSSL)", "84" },
                              { "KRTX (Portland)", "86" },
                              { "KPDT (Pendleton)", "86" },
                              { "KMAX (Medford)", "86" },
                              { "KCCX (State College)", "81" },
                              { "KPBZ (Pittsburgh)", "81" },
                              { "KDIX (Philadelphia)", "81" },
                              { "TJUA (San Juan)", "82" },
                              { "KGSP (Greer)", "82" },
                              { "KCAE (Columbia)", "82" },
                              { "KCLX (Charleston)", "82" },
                              { "KFSD (Sioux Falls)", "83" },
                              { "KUDX (Rapid City)", "83" },
                              { "KABR (Aberdeen)", "83" },
                              { "KOHX (Nashville)", "84" },
                              { "KNQA (Memphis)", "84" },
                              { "KMRX (Knoxville/Tri Cities)", "84" },
                              { "KSJT (San Angelo)", "84" },
                              { "KMAF (Midland/Odessa)", "84" },
                              { "KLBB (Lubbock)", "84" },
                              { "KDFX (Laughlin AFB)", "84" },
                              { "KHGX (Houston/Galveston)", "84" },
                              { "KGRK (Fort Hood)", "84" },
                              { "KEPZ (El Paso)", "84" },
                              { "KDYX (Dyess AFB)", "84" },
                              { "KFWS (Dallas/Ft. Worth)", "84" },
                              { "KCRP (Corpus Christi)", "84" },
                              { "KBRO (Brownsville)", "84" },
                              { "KEWX (Austin/San Antonio)", "84" },
                              { "KAMA (Amarillo)", "84" },
                              { "KMTX (Salt Lake City)", "85" },
                              { "KICX (Cedar City)", "85" },
                              { "KLWX (Sterling)", "81" },
                              { "KFCX (Roanoke)", "81" },
                              { "KAKQ (Norfolk/Richmond)", "81" },
                              { "KCXX (Burlington)", "81" },
                              { "KOTX (Spokane)", "86" },
                              { "KATX (Seattle/Tacoma)", "86" },
                              { "KLGX (Langley Hill)", "86" },
                              { "KMKX (Milwaukee)", "83" },
                              { "KARX (La Crosse)", "83" },
                              { "KGRB (Green Bay)", "83" },
                              { "KRLX (Charleston)", "81" },
                              { "KRIW (Riverton)", "85" },
                              { "KCYS (Cheyenne)", "85" },
                              { "RKSG (Camp Humpreys)", "00" },
                              { "RKJK (Kunsan AB)", "00" },
                              { "RODN (Kadena AB)", "00" },
                              { "", ""} };


#endif	/* #ifndef WMO_AWIPS_HDR_H */
