package main

import (
	"fmt"
	"bytes"
	"regexp"
	"strings"
	"net/url"
	"net/http"
	"io"
	"os"
)

var println = fmt.Println

var row = regexp.MustCompile("<tr class=.+?>(.*?)</tr>")
var column = regexp.MustCompile("hideIt2.+?;'>(.*?)</a>")

func basicParse(reader io.Reader){
	buf := new(bytes.Buffer)
	n, err := buf.ReadFrom(reader)
	if err!=nil{
		println("error in basicParse: ")
		println(err)
		return
	}
	println(n, " bytes read from body")
	s := strings.Replace(buf.String(), "\n", "", -1)
/*	
	index := strings.Index(s, "<tbody>")
	index2 := strings.Index(s, "</tbody>")
	println("index = ", index, ", index2 = ", index2)
	substr := s[index+7 :index2]
*/
	
	matches := row.FindAllStringSubmatch(s, -1)
	if matches != nil{
	
		fd, err := os.Create("BasicInfo_otc.json")
		if err !=  nil{
			println(err)
			return
		}else{
			println(len(matches), " match(es) get")
			for _, m := range(matches){				//for each company
				println("----------------------")
				fd.WriteString("{\n")
				
				//println(m[1])
				items := column.FindAllStringSubmatch(m[1], -1)
				if items != nil {
					for i, item := range(items){
						tmp := item[1]
						result := ""
						println(tmp)
						
						switch(i){	
							case 0:
								result = fmt.Sprintf("\"id\": \"%s\",\n", tmp)
							case 1:
								result = fmt.Sprintf("\"abbr1\": \"%s\",\n", tmp)
							case 2:
								result = fmt.Sprintf("\"abbr2\": \"%s\",\n", tmp)
							case 3:
								result = fmt.Sprintf("\"name\": \"%s\",\n", tmp)
							case 4:
								result = fmt.Sprintf("\"market\": \"%s\",\n", tmp)
							case 5:
								result = fmt.Sprintf("\"industry\": \"%s\",\n", tmp)
							case 6:
								result = fmt.Sprintf("\"note\": \"%s\"\n", tmp)
							default:
								result = ""
						}
						fd.WriteString(result)
					}
				}
				fd.WriteString("},\n")
			}//end for
			fd.Close()
		}
	}else{
		println("No match: no table rows.")
	}
}

func main(){
	target := "http://mops.twse.com.tw/mops/web/ajax_quickpgm" 
	otcForm := url.Values{
		"encodeURIComponent" : {"1"},
		"firstin" : {"true"},
		"step" : {"4"},
		"checkbtn" : {"1"},
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
	
	println(res.Status)
	//fmt.Print(res.Header)
	basicParse(res.Body)
}
	
	