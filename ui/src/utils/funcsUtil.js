// 抛出公共的函数

const deepCopy = (obj) => {
    return JSON.parse(JSON.stringify(obj));
};

const generateRandomString = (length) => {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters.charAt(randomIndex);
    }

    return result;
}

const publishTimeFormat = (date) => {
    date = date.toString()
    // return date.substring(0, 4) + "年" + date.substring(4, 6) + "月" + date.substring(6, 8) + "日"
    return date.substring(0, 4) + "-" + date.substring(4, 6) + "-" + date.substring(6, 8)
}

export {
    deepCopy, generateRandomString, publishTimeFormat
}