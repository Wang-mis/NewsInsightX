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

export {
    deepCopy, generateRandomString
}