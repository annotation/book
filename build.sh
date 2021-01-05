#!/bin/sh

book=corpus_computing_with_text_fabric


if [[ "$1" == "clean" ]]; then
    jb clean $book/
fi

jb build $book/
cp -r $book/uruk/cdli-imagery $book/_build/html/uruk
cp $book/_static/mystnb.css $book/_build/html/_static
