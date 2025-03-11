
activate_venv () {
    python -m venv .venv
    source ./.venv/bin/activate
}

activate () {
    if [[ $1 = "new" ]]; then
        echo "Deleting venv and starting"
        deactivate
        rm -rf .venv
        activate_venv
    elif [ -d ".venv" ]; then
        echo "Enabling venv"
        activate_venv
    else
        echo "Making venv and enabling"
        activate_new
    fi
}

# call the function with activate_venv () and activate () because I don't have it in .zshrc