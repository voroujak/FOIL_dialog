
0.8::father(john, mary).
0.7::father(john, billy).

mother(mary, tom).
mother(an, jenny).

parent(X,Y) :- mother(X,Y).
parent(X,Y) :- father(X,Y).

0.8::grandfather(john, tom).
 
 
base(father(person,person)).
base(mother(person,person)).
base(parent(person,person)).
base(grandfather(person,person)).


mode(father(+,-)).
mode(mother(+,-)).



learn(grandfather/2). 




