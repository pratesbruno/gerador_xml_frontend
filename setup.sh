mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"dados@beepsaude.com.br\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml

echo "\
[theme]\n\
base=\"light\"\n\
primaryColor=\"#00afaa\"\n\
" > ~/.streamlit/config.toml
