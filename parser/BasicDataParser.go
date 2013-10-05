package main

import "fmt"
import "bytes"
import "strings"
import "net/url"
import "net/http"
import "io"

var println = fmt.Println

func basicParse(reader io.Reader){
	buf := new(bytes.Buffer)
	n, err := buf.ReadFrom(reader)
	if err!=nil{
		println("error in basicParse: ")
		println(err)
		return
	}
	println(n, " bytes read from body")
	s := buf.String()
	
	index := strings.Index(s, "<tbody>")
	index2 := strings.Index(s, "</tbody>")
	println("index = ", index, ", index2 = ", index2)
	//substr := s[index+7 :index2]
	
	println(s)
}

func main(){
	target := "http://mops.twse.com.tw/mops/web/ajax_quickpgm" 
	otcForm := url.Values{
		"encodeURIComponent" : {"1"},
		"firstin" : {"true"},
		"step" : {"4"},
		"checkbtn" : {"0"},
		"queryName" : {"co_id"},
		"TYPEK2" : {"otc"},
		"code1" : {""},
		"keyword4" : {""}}

	println("=== Data Parser for Taiwan Listed Companise ===")
	println("start parsing...")
	res, err := http.PostForm(target, otcForm)
	
	if err != nil{
		println(err)
		return
	}
	
	fmt.Println(res.Status)
	basicParse(res.Body)
}
	
	