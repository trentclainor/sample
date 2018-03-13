export function checkHttpStatus(response) {
    if (response.status >= 200 && response.status < 300) {
        return response;
    }

    const error = new Error(response.statusText);
    error.response = response;
    throw error;
}

export function getOrderingParams(ordering){
    let orderingParams = {};
    if (ordering){
        orderingParams['ordering'] = ordering;
    }
    return orderingParams
}

export function getPaginationParams(limit, offset){
    let paginationParams = {};
    if (limit){
        paginationParams['limit'] = limit;
    }
    if (offset){
        paginationParams['offset'] = offset;
    }
    return paginationParams
}


export function prepareParams(filtering, ordering, limit, offset){
    let orderingParams = getOrderingParams(ordering);
    let paginationParams = getPaginationParams(limit, offset);
    return Object.assign({}, filtering, orderingParams, paginationParams);
}

export function filterObjectByKey(object, excludeKeys) {
    let result = {};
    Object.keys(object).forEach(key => excludeKeys.indexOf(key) === -1 ? result[key] = object[key] : null);
    return result;
}

export function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

export function range(start, end) {
    let foo = [];
    for (let i = start; i <= end; i++) {
        foo.push(i);
    }
    return foo;
}
