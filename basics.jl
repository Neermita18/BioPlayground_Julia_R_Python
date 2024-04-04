col= [1,2, 5,6]
println(col)
println(col[:3])
print(col[1:3])
append!(col, 9)
println(col)
println(col[2:end]) # 2 5 6
println(col[end-1]) #5
@show col
col2= col
col2[2]=89
println(col) #col changes too?!
colcop= copy(col)
colcop[3]=56
@show col #now no change in col
@show colcop

# tuples: immutable
tuple1= (1,2,4)
# immutable
@show (tuple1)

# named tuples
tools= (lang="julia", ide="pluto")
println(tools)
println(tools[1])
println(tools.lang)

# dictionaries
d= Dict("lang" => "julia", "ide" => "pluto")
println(d)
println(d["lang"])
d["ide"]="changed"
@show d
pop!(d) #pops first element
@show d