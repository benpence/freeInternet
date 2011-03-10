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
   Author   : Manish Jain (jain@cc.gatech.edu)
              Constantinos Dovrolis (dovrolis@cc.gatech.edu)
   Release  : Ver 1.3.2
   Support  : This work was supported by the SciDAC
              program of the US department 
--------------------------------------------------*/
#define LOCAL
#include "pathload_gbls.h"
#include "pathload_snd.h"

int main(int argc, char* argv[])
{
  struct hostent *host_rcv;
  struct timeval tv1,tv2;
  l_uint32 snd_time ;
  l_int32 ctr_code ;
  time_t localtm;
  int opt_len,mss;
  int ret_val ;
  int iterate=0;
  int done=0;
  int latency[30],ord_latency[30];
  int i;
  int c ;
  int errflg=0;
  char pkt_buf[256];
  char ctr_buff[8];

  quiet=0;
  while ((c = getopt(argc, argv, "ihHq")) != EOF)
    switch (c) 
    {
      case 'H':
      case 'h':
        help() ;
        break ;
      case 'i':
        iterate=1;
        break;
      case 'q':
        quiet=1;
        break;
      case '?':
        errflg++;
    }
  if (errflg)
  {
    fprintf(stderr, "usage: pathload_snd [-q] [-H|-h]\n");
    exit(-1);
  }

  num_stream = NUM_STREAM ;
  min_sleeptime();

  /* gettimeofday latency */
  for(i=0;i<30;i++)
  {
    gettimeofday(&tv1,NULL);
    gettimeofday(&tv2,NULL);
    latency[i]=tv2.tv_sec*1000000+tv2.tv_usec-tv1.tv_sec*1000000-tv1.tv_usec;
  }
  order_int(latency,ord_latency,30);
  gettimeofday_latency = ord_latency[15];  
#ifdef DEBUG
  printf("DEBUG :: gettimeofday_latency = %d\n",gettimeofday_latency);
#endif
  /* Control stream: TCP connection */
  if ((sock_tcp=socket(AF_INET, SOCK_STREAM, 0)) < 0)
  {
    perror("socket(AF_INET,SOCK_STREAM,0):");
    exit(-1);
  }
  opt_len=1;
  if (setsockopt(sock_tcp, SOL_SOCKET, SO_REUSEADDR, (char*)&opt_len, 
        sizeof(opt_len)) < 0)
  {
    perror("setsockopt(SOL_SOCKET,SO_REUSEADDR):");
    exit(-1);
  }
  bzero((char*)&snd_tcp_addr, sizeof(snd_tcp_addr));
  snd_tcp_addr.sin_family         = AF_INET;
  snd_tcp_addr.sin_addr.s_addr    = htonl(INADDR_ANY);
  snd_tcp_addr.sin_port           = htons(TCPSND_PORT);
  if (bind(sock_tcp, (struct sockaddr*)&snd_tcp_addr,sizeof(snd_tcp_addr)) < 0)
  {
    perror("bind(sock_tcp):");
    exit(-1);
  }
  if (listen(sock_tcp,1) < 0)
  {
    perror("listen(sock_tcp,1):");
    exit(-1);
  }
  /* Data stream: UDP socket */
  if ((sock_udp=socket(AF_INET, SOCK_DGRAM, 0)) < 0)
  {
    perror("socket(AF_INET,SOCK_DGRAM,0):");
    exit(-1);
  }
  bzero((char*)&snd_udp_addr, sizeof(snd_udp_addr));
  snd_udp_addr.sin_family         = AF_INET;
  snd_udp_addr.sin_addr.s_addr    = htonl(INADDR_ANY);
  snd_udp_addr.sin_port           = htons(0);
  if (bind(sock_udp, (struct sockaddr*)&snd_udp_addr, 
        sizeof(snd_udp_addr)) < 0)
  {
    perror("bind(sock_udp):");
    exit(-1);
  }
  send_buff_sz = UDP_BUFFER_SZ;
  if (setsockopt(sock_udp, SOL_SOCKET, SO_SNDBUF, (char*)&send_buff_sz, 
        sizeof(send_buff_sz)) < 0)
  {
    send_buff_sz/=2;
    if (setsockopt(sock_udp, SOL_SOCKET, SO_SNDBUF, (char*)&send_buff_sz, 
        sizeof(send_buff_sz)) < 0)
    {
      perror("setsockopt(SOL_SOCKET,SO_SNDBUF):");
      exit(-1);
    }
  }
  do
  {
    if ( !quiet)
      printf("\n\nWaiting for receiver to establish control stream => ");
    fflush(stdout);
    /* 
      Wait until receiver attempts to connect, 
      starting new measurement cycle
    */
    rcv_tcp_adrlen = sizeof(rcv_tcp_addr);
    ctr_strm = accept(sock_tcp, (struct sockaddr*)&rcv_tcp_addr, &rcv_tcp_adrlen);
    if (ctr_strm < 0)
    {
      perror("accept(sock_tcp):");
      exit(-1);
    }  
    if ( !quiet)
      printf("OK\n");
    localtm = time(NULL); 
    gethostname(pkt_buf, 256);
    host_rcv=gethostbyaddr((char*)&(rcv_tcp_addr.sin_addr), sizeof(rcv_tcp_addr.sin_addr), AF_INET);
    if (host_rcv!=NULL)
    {
      if ( !quiet)
        printf("Receiver %s starts measurements on %s", host_rcv->h_name, ctime(&localtm));
    }
    else
      if ( !quiet)
        printf("Unknown receiver starts measurements at %s", ctime(&localtm));

    /* Form receiving UDP address */
    bzero((char*)&rcv_udp_addr, sizeof(rcv_udp_addr));
    rcv_udp_addr.sin_family         = AF_INET;
    rcv_udp_addr.sin_addr.s_addr    = rcv_tcp_addr.sin_addr.s_addr;
    rcv_udp_addr.sin_port           = htons(UDPRCV_PORT);
    /* Connect UDP socket */
    connect(sock_udp , (struct sockaddr *)&rcv_udp_addr , sizeof(rcv_udp_addr)); 
    /* Make TCP socket non-blocking */
    if (fcntl(ctr_strm, F_SETFL, O_NONBLOCK)<0)
    {
      perror("fcntl(ctr_strm, F_SETFL, O_NONBLOCK):");
      exit(-1);
    }
    opt_len = sizeof(mss) ;
    if (getsockopt(ctr_strm, IPPROTO_TCP, TCP_MAXSEG, (char*)&mss, &opt_len)<0)
    {
      perror("getsockopt(sock_tcp,IPPROTO_TCP,TCP_MAXSEG):");
      exit(-1);
    }
    snd_max_pkt_sz = mss;
    if (snd_max_pkt_sz == 0 || snd_max_pkt_sz== 1448) 
      snd_max_pkt_sz = 1472;   /* Make it Ethernet sized MTU */
    else
      snd_max_pkt_sz = mss+12;

    /* tell receiver our max packet sz */
    send_ctr_mesg(ctr_buff, snd_max_pkt_sz) ;
    /* receiver's maxp packet size */
    while ((rcv_max_pkt_sz = recv_ctr_mesg( ctr_buff)) == -1);
    max_pkt_sz = (rcv_max_pkt_sz < snd_max_pkt_sz) ? rcv_max_pkt_sz:snd_max_pkt_sz ;
    if ( !quiet )
      printf("Maximum packet size          :: %ld bytes\n",max_pkt_sz);
    /* tell receiver our send latency */
    snd_time = (l_int32) send_latency();
    send_ctr_mesg(ctr_buff, snd_time) ;

    /* wait for receiver to start ADR measurement */
    if((ret_val=recv_ctr_mesg(ctr_buff)) == -1 )break;
    if ( (((ret_val & CTR_CODE) >> 31) == 1) && ((ret_val & 0x7fffffff) == SEND_TRAIN ) ) 
    {
      if ( !quiet)
        printf("Estimating ADR to initialize rate adjustment algorithm => ");
      fflush(stdout);
      if ( send_train() == -1 ) continue ;
      if ( !quiet)
        printf("Done\n");
    }
    fleet_id=0;
    done=0;
    /* Start avail-bw measurement */
    while(!done)
    {
      if (( ret_val  = recv_ctr_mesg ( ctr_buff ) ) == -1 ) break ;
      if((((ret_val & CTR_CODE) >> 31) == 1) &&((ret_val&0x7fffffff) == TERMINATE)) 
      {
        if ( !quiet)
          printf("Terminating current run.\n");
        done=1;
      }
      else
      {
        transmission_rate = ret_val ;
        if ((cur_pkt_sz = recv_ctr_mesg( ctr_buff)) <= 0 )break;
        if ((stream_len = recv_ctr_mesg( ctr_buff))  <= 0 )break;
        if ((time_interval = recv_ctr_mesg( ctr_buff)) <= 0 )break;
        if ((ret_val = recv_ctr_mesg ( ctr_buff )) == -1 )break;
        /* ret_val = SENd_FLEET */
        ctr_code = RECV_FLEET | CTR_CODE ;
        if ( send_ctr_mesg(ctr_buff,  ctr_code  ) == -1 ) break;
        if(send_fleet()==-1) break ;
        if ( !quiet) printf("\n");
        fleet_id++ ;
      }
    }
    close(ctr_strm);
  }while (iterate);
  
  return 0;
}

