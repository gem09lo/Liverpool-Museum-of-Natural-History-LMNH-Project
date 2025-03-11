commit () {
    git fetch
    git pull
    git_status=$(git status)
    if [[ "$git_status" != *"nothing to commit"* ]]
        git add .
        echo "Commit message:"
        read msg
        git commit -m "$msg"
        git push
    fi

}

# commit ()