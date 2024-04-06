f= "cholerae.txt"

open(f) do file
    text=""
    for line in eachline(file)
        text=line
       
    end
    # print(text)
    function isA(c)
        return c=='A'
    end

    A= count(isA, text)
    println("number of adenine molecules: ",A)
    C= count(x->x=='C', text)
    
    println("number of cytosine molecules: ",C)
    T= count(x->x=='T', text)
    
    println("number of thymine molecules: ",T)
    G= count(x->x=='G', text)
    
    println("number of guanine molecules: ",G)
    print("Total number of molecules: ",length(text))
end


