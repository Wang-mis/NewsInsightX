export const deepCopy = (obj) => {
    return JSON.parse(JSON.stringify(obj));
};

export const publishTimeFormat = (date) => {
    date = date.toString()
    return date.substring(0, 4) + "-" + date.substring(4, 6) + "-" + date.substring(6, 8)
}
