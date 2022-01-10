select date(ts) as ts,ip,round(sum(cpu_usage)/count(*),2) as avg_cpu_usage, max(cpu_usage) as max_cpu_usage,min(cpu_usage)
 as min_cpu_usage, round(sum(mem_usage)/count(*),2) as avg_mem_usage,max(mem_total_mb) as total_mem_total,max(mem_usage)
 as max_mem_usage,min(mem_usage) as min_mem_usage,round(sum(mem_avail_mb)/count(*),2) as avg_mem_avail,max(mem_avail_mb)
 as max_mem_avail,min(mem_avail_mb) as min_mem_avail  from data_hour where date(ts) =  current_date
group by date(ts),ip order by max(cpu_usage) asc

create view view_report as
select date(ts) as ts,ip,round(sum(cpu_usage)/count(*),2) as avg_cpu_usage, max(cpu_usage) as max_cpu_usage,min(cpu_usage)
 as min_cpu_usage, round(sum(mem_usage)/count(*),2) as avg_mem_usage,max(mem_total_mb) as total_mem_total,max(mem_usage)
 as max_mem_usage,min(mem_usage) as min_mem_usage,round(sum(mem_avail_mb)/count(*),2) as avg_mem_avail,max(mem_avail_mb)
 as max_mem_avail,min(mem_avail_mb) as min_mem_avail  from data_hour where date(ts) =  current_date
group by date(ts),ip order by max(cpu_usage) asc

create view view_report2 as select ipmax_cpu_usage,min_mem_avail from view_report order by min_mem_avail desc ;
create view view_mem as select ip,avg_mem_usage,total_mem_total,max_mem_usage,min_mem_avail from view_report order by avg_mem_usage,
create view view_emr as select * from view_report2 where ip in('10.40.1.142','10.40.1.117','10.40.1.18','10.40.1.177');

select  ip,round(sum(cpu_usage)/count(*),2) as avg_cpu_usage, max(cpu_usage) as max_cpu_usage,min(cpu_usage)
 as min_cpu_usage, round(sum(mem_usage)/count(*),2) as avg_mem_usage,max(mem_total_mb) as total_mem_total,max(mem_usage)
 as max_mem_usage,min(mem_usage) as min_mem_usage,round(sum(mem_avail_mb)/count(*),2) as avg_mem_avail,max(mem_avail_mb)
 as max_mem_avail,min(mem_avail_mb) as min_mem_avail  from data_hour
group by ip order by max(cpu_usage) asc

create view view_mem as
select ip,avg_mem_usage,max_mem_usage,total_mem_total, round((avg_mem_usage * total_mem_total) / 100,2) as program_mem_usage,
   round(total_mem_total - ((avg_mem_usage * total_mem_total) / 100) - min_mem_avail,2)   as   cache_mem_usage,min_mem_avail,
 round(total_mem_total - ((avg_mem_usage * total_mem_total) / 100),2) as max_mem_avail from view_report order by min_mem_avail desc

10.40.1.204 当前可用内存 11529 MB
10.40.0.202 当前可用内存 7307 MB


sqlite3 watch.db -header -column "select * from view_mem"