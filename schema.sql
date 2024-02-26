drop table if exists tasks;
create table tasks (
  id integer primary key autoincrement,
  task_names text not null,
  'text' text not null
);