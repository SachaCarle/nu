const type_grammar_parser = {
    symbol: (token, grammar) => {
        if (grammar.symbol === true) return token.value;
        else if (grammar.symbol === token.value) return true;
        return false;
    },
    char: (token, grammar) => {
        if (grammar.char === true) return token.value;
        else if (grammar.char === token.value) return true;
        return false;
    },
    EOL: (token, grammar) => {
        if (grammar.EOL === true) return true;
        else if (grammar.EOL === token.value) return true;
        return false;
    },
    container: (token, grammar) => {
        if (grammar.container[0] !== token.value[0]) return false;
        if (grammar.container[grammar.container.length - 1] !== token.value[token.value.length - 1]) return false;
        return {
            value: token.value.slice(1, token.value.length - 1),
            grammar: grammar.container.slice(1, grammar.container.length - 1)
        }
    }
}

function parse_token_grammar(token, grammar) {
    for (let attr_name in grammar) {
        if (token.type === attr_name) {
            let res = type_grammar_parser[attr_name](token, grammar);
            if (res !== false) {
                return res;
            }
        }
    }
    return false;
}

function parse_tokens_with_grammar(tokens, grammar) {
    if (tokens.length < grammar.length) return false;
    let result = [];
    let i = 0;
    let j = 0;
    while (i < grammar.length) {
        let o = parse_token_grammar(tokens[j], grammar[i]);
        // NULL & CHAIN
        if (o === false) return false;
        result.push(o);
        i += 1;
        j += 1;
    }
    return result;
}

export {
    parse_token_grammar,
    parse_tokens_with_grammar
};