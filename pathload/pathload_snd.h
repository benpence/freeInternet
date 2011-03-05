/*
 This file is part of pathload.

 pathload is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 pathload is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with pathload; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
*/

/*-------------------------------------------------
   pathload : an end-to-end available bandwidth 
              estimation tool
   Author   : Manish Jain ( jain@cc.gatech.edu )
              Constantinos Dovrolis (dovrolis@cc.gatech.edu )
   Release  : Ver 1.3.2
   Support  : This work was supported by the SciDAC
              program of the US department 
--------------------------------------------------*/

/* 
 * $Header: /net/cvs/bwtest/pathload/pathload_snd.h,v 1.38 2006/05/19 19:12:27 jain Exp $
 */
#ifdef LOCAL
#define EXTERN
#else
#define EXTERN extern
#endif

EXTERN int send_fleet() ;
EXTERN int send_train();
EXTERN int send_ctr_mesg(char *ctr_buff, l_int32 ctr_code);
EXTERN l_int32 recv_ctr_mesg( char *ctr_buff);
EXTERN l_int32 send_latency() ;
EXTERN void min_sleeptime() ;
EXTERN void order_int(int unord_arr[], int ord_arr[], int num_elems);
EXTERN double time_to_us_delta(struct timeval tv1, struct timeval tv2);
EXTERN l_int32 fleet_id_n ;
EXTERN l_int32 fleet_id  ;
EXTERN int sock_udp, sock_tcp, ctr_strm, send_buff_sz, rcv_tcp_adrlen;
EXTERN struct sockaddr_in snd_udp_addr, snd_tcp_addr, rcv_udp_addr, rcv_tcp_addr;
EXTERN l_int32 min_sleep_interval ; /* in usec */
EXTERN l_int32 min_timer_intr ; /* in usec */
EXTERN int gettimeofday_latency ;

EXTERN void order_dbl(double unord_arr[], double ord_arr[],int start, int num_elems);
EXTERN void order_float(float unord_arr[], float ord_arr[],int start, int num_elems);
EXTERN void order_int(int unord_arr[], int ord_arr[], int num_elems);
EXTERN void help() ;
EXTERN int quiet ;
