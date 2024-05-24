fi="input.txt"
text = String[]
open(fi) do file
   for line in eachline(file) 
    textl=line
    push!(text, textl)
   end
   
end
println(text)
t= text[1]
println(t)
@show t
p=text[2]
global c=0
for i in 1:(length(t) - length(p) + 1)
   
   
   if t[i:i+length(p)-1] == p
       
      global c+=1
   end

end
println(c)

