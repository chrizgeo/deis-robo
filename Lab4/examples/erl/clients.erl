-module(clients).
-export([start/3, client/2]).

start(ServiceID, N, M) ->
   lists:foreach(
     fun (Num) -> spawn(clients, client, [ServiceID, Num]), timer:sleep(250) end,
     lists:seq(N, M)).

client(ServiceID, Num) ->
  ServiceID ! Num, timer:sleep(1000), client(ServiceID, Num).
