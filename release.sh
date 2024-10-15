#!/usr/bin/env bash

if ! command -v typos &>/dev/null; then
  echo "typos is not installed. Run 'cargo install typos-cli' to install it, otherwise the typos won't be fixed"
fi

if [ -z "$1" ]; then
	echo "Please provide a tag."
	echo "Usage: ./release.sh v[X.Y.Z]-[suffix]"
	exit
fi

echo "Preparing $1..."
msg="# managed by release.sh"

# update the changelog
git-cliff --config .cliff/default.toml --tag "$1" > CHANGELOG.md
git add -A && git commit -m "chore(release): prepare for $1"
git show

# generate a changelog for the tag message
export GIT_CLIFF_TEMPLATE="\
	{% for group, commits in commits | group_by(attribute=\"group\") %}
	{{ group | upper_first }}\
	{% for commit in commits %}
		- {% if commit.breaking %}(breaking) {% endif %}{{ commit.message | upper_first }} ({{ commit.id | truncate(length=7, end=\"\") }})\
	{% endfor %}
	{% endfor %}"

changelog=$(git-cliff --config .cliff/detailed.toml --unreleased --strip all)

git tag -s -a "$1" -m "Release $1" -m "$changelog"
git tag -v "$1"

# Extract the date and suffix
today=$(date +%d.%m.%Y)
suffix=$(echo "$1" | cut -d'-' -f2-)

# Update README.md with the new release information
if [ -n "$suffix" ]; then
    echo "Updating README.md with version information..."
    release_info="[$today - $suffix](https://github.com/Flokkq/dsai_24-25/releases/tag/$1)"
    echo "- $release_info" >> README.md
    git add README.md
    git commit -m "chore(docs): update README.md with release $1"
fi

echo "Done!"
echo "Now push the commit (git push) and the tag (git push --tags)."
