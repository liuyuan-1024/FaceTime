import requests from '@/api/request'

// 记录信息
export function recordInformation(userId: number, userName: string) {
    return requests.post('/user/recordInformation', {
        userId,
        userName
    })
}

// 用户签到
export async function signIn() {
    return requests.get('/user/signIn')
}

// 记录信息
export function recordInformation2(userId: number, userName: string, base64image: string) {
    return requests.post('/user/recordInformation2', {
        userId,
        userName,
        base64image
    })
}

// 用户签到
export async function signIn2(base64image: string) {
    return requests.post('/user/signIn2', {
        base64image
    })
}
