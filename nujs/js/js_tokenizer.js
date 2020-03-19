/* eslint-disable no-console */
let default_tokens = {
    m: 'abcdefghijklmnopqrstuvwxyz',
    M: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    symbol_nalpha: '_$0123456789',
    open: '{([',
    close: '})]',
    // < & > are operators and open/close
    comment_open: ['/*', '<!--', '"""', "'''"],
    comment_close: ['*/', '-->', '"""', "'''"],
    comment_line: ['//', '#'],
    string: "\"'`",
    EOL: '\n',
}

/*
function tokenizer_multiple_char(sa, i, sb, returnFalseOnEndFIle = true) {
    let k = 0;
    while (k < sb.length) {
        if (i + k >= sa.length)
            if (returnFalseOnEndFIle) return false
            else throw Error('EOF')
        if (sa[i + k] !== sb[k]) {
            return false;
        }
        k += 1;
    }
    return true;

}


function tokenizer_comments(ts, str, i, tokens) {
    let j = 0;
    while (j < tokens.comment_line.length) {
        if (tokenizer_multiple_char(str, i, tokens.comment_line[j])) {
            console.log(tokens.comment_line[j]);
            let obj = {
                index: i,
                type: 'comment',
                value: tokens.comment_line[j]
            }
            i += tokens.comment_line[j].length;
            while (str[i] != tokens.EOL && i < str.length) {
                obj.value += str[i];
                i += 1;
            }
            ts.push(obj);
            return tokenizer_comments(ts, str, i, tokens);
        }
    } // COMMENTS LINE
    j = 0;
    while (j < tokens.comment_open.length) {
        if (tokenizer_multiple_char(str, i, tokens.comment_open[j])) {
            console.log(tokens.comment_open[j]);
            let obj = {
                index: i,
                type: 'comment',
                value: tokens.comment_open[j]
            }
            i += tokens.comment_open[j].length;
            try {
                while (!(tokenizer_multiple_char(str, i, tokens.comment_close[j], false))) {
                    obj.value += str[i];
                    i += 1;
                }
                ts.push(obj);
                return tokenizer_comments(ts, str, i, tokens);
            } catch (error) {
                throw Error("Unexpected error during comment parsing at index " + i + ": " + error.toString());
            }
        }
    } // COMMENTS OPEN CLOSE

    return i;
}
*/

function tokenizer(str, tokens = default_tokens) {
    console.error("Tokeniz! ", str)
    let ts = [];
    let i = 0;
    while (i < str.length) {
        let _type = 'char';
        //i = tokenizer_comments(ts, str, i, tokens);
        // IL FAUT UNE AUTRE SOLUTION :()
        if (tokens.m.includes(str[i]) || tokens.M.includes(str[i])) {
            let obj = { type: 'symbol', index: i, value: '' };
            while (tokens.m.includes(str[i]) || tokens.M.includes(str[i]) || tokens.symbol_nalpha.includes(str[i])) {
                obj.value += str[i];
                i += 1;
                if (i == str.length)
                    break;
            }
            ts.push(obj);
            continue; // i += 1;
        } else if (tokens.open.includes(str[i])) {
            let obj = { type: 'container', index: i, value: '' };
            let opener = str[i];
            let closer = tokens.close[tokens.open.indexOf(opener)];
            let counter = 0;
            while (closer != str[i] || counter != 0) {
                if (closer == str[i] && counter >= 1)
                    counter -= 1;
                obj.value += str[i];
                i += 1;
                if (i == str.length)
                    throw Error('Unmatched ' + opener + ' abort tokenization');
                else if (opener == str[i])
                    counter += 1;
            }
            obj.value += str[i];
            i += 1;
            ts.push(obj);
            continue;
        } else if (tokens.string.includes(str[i])) {
            let obj = { type: 'literal_string', index: i, value: str[i] };
            let literal = str[i];
            i += 1;
            while (str[i] != literal) {
                if (str[i] == '\\' && str[i + 1] == literal) {
                    obj.value += '\\' + literal;
                    i += 2;
                }
                obj.value += str[i];
                i += 1;
                if (i == str.length)
                    throw Error('Unmatched ' + literal + ' abort tokenization');
            }
            obj.value += str[i];
            i += 1;
            ts.push(obj);
            continue;
        } else if (tokens.EOL.includes(str[i])) {
            _type = 'EOL';
        }
        ts.push({
            type: _type,
            index: i,
            value: str[i],
        });
        i += 1; // continue
    }
    return ts;
}

function listen(chunk) {
    if (!chunk) {
        return
    }
    res = tokenizer(chunk)
    console.log(JSON.stringify(res))
    return res
}

module.exports = listen