#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using std::cout;
using std::endl;
using std::string;
using std::ifstream;
using std::cerr;
using std::vector;

vector<string> tokens;

string get_code_string(string file_name){
	ifstream file(file_name);
    if (!file.is_open()){
        cerr << "[ERRROR] Archivo no encontrado" << endl;
        return "";
    }
	string code = "";
	string line;
    while(getline(file, line)){
		line += ' ';
		code += line;
    }
    file.close();
	return code;
}

void tokenize(string code){
	string token = "";
	bool literal_string = false;

	for(char c : code){
		if(c == '\t') continue;

		if(c == '"'){
			literal_string = !literal_string;
		}

		if(c == ' '){
			if(!literal_string){
				tokens.push_back(token);
				token = "";
			}else{
				token += ' ';
			}
		}else{
			token += c;
		}
	}
	tokens.push_back(token);
}

string process_code(){
	string data = "";
	string code = ".code\nmov ax, @data\nmov ds, ax\nprint macro s\nmov ah, 9h\nlea dx, s\nint 21h\nendm\n";

	for(int i = 0; i < tokens.size(); i++){
		string token = tokens[i];

		if(token == "whencuando"){
			data += ".model small\n.stack\n.data\n";
		}else

		if(token == ":v"){
			token = tokens[++i];
			if(token[0] == '"'){
				token = token.substr(1, token.length()-2);
				data += "s" + std::to_string(i) + " db '" + token + "', 10, '$'\n";
				code += "print s" + std::to_string(i) + "\n";
			}else{
				//Caso para variables
			}
		}else

		if(token == "var"){
			token = tokens[++i];
			string nm = token;
			token = tokens[++i];
			token = tokens[++i];
			data += nm + " db " + token + "\n";
		}else
		
		if(token == "xdxd"){
			code += "int 27h\nend";
		}
	}

	data += code;
	return data;
}

int main(){
	string code = get_code_string("tests/hello.cmt");
	tokenize(code);
	string final_code = process_code();
	cout << final_code;
    return 0;
}