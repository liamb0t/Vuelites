export type QueryParams = {
    sort: 'top' | 'new' | 'hot'
    time: 'all' | 'day' | 'hour' | 'month' | 'week' | 'year'
    after: string
}
