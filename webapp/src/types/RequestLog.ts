import type {NameValuePairs} from "@/types/common";

export type RequestLogBody = {
    length: number;
    hash: string | null;
    contentType?: string | null;
    previewContent?: string | null;
    mimeType?: string | null;
}

export type HttpHeaders = NameValuePairs;

export enum RequestLogPhase {
    BEGIN = 'requestHead',
    REQUEST_HEAD = 'requestHead',
    REQUEST_BODY_READING = 'requestBodyReading',
    REQUEST_FORWARD = 'requestForward',
    RESPONSE_BODY_READING = 'responseBodyReading',
    RESPONSE_BODY_READ = 'responseBodyRead',
    END = 'end',
}

export type HttpUrlQueryParameters = NameValuePairs;

export type RequestLogException = {
    message: String,
    traceback: String,
    type: String,
}

export type RequestLog = {
    phase: RequestLogPhase;
    time: number;
    lastTime: number;
    id: number;
    exception?: RequestLogException,
    request?: {
        method: string;
        url: string;
        headers?: HttpHeaders;
        body?: RequestLogBody;
        queryParameters?: HttpUrlQueryParameters,
    };
    response?: {
        status: number;
        headers?: HttpHeaders;
        body?: RequestLogBody;
    } | null;
    forwardDestination?: string | null;
}
