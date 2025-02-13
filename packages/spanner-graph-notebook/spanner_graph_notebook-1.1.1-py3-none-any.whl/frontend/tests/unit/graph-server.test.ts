/**
 * Copyright 2025 Google LLC
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import path from "path";
import fs from "fs";

// @ts-ignore
const GraphServer = require('../../src/graph-server');

describe('GraphServer', () => {
    let graphServer: typeof GraphServer;
    const mockFetch = jest.fn();
    global.fetch = mockFetch;

    beforeEach(() => {
        mockFetch.mockClear();
        graphServer = new GraphServer(
            8000,
            {'project': 'test-project',
             'instance': 'test-instance',
             'database': 'test-database',
             'mock': false
            }
        );
    });

    describe('constructor', () => {
        it('should initialize with the default variables', () => {
           expect(graphServer.port).toBe(8000);
           expect(graphServer.params).toStrictEqual(
            {'project': 'test-project',
             'instance': 'test-instance',
             'database': 'test-database',
             'mock': false
           });
        });

        it('should fail to initialize when no port is provided', () => {
            console.error = jest.fn();

            const defaultServer = new GraphServer(
                null,
                {}
            );

            expect(console.error).toHaveBeenCalledWith('Graph Server was not given a numerical port', {port: null});
        });

        it('should cast a string port to a number', () => {
            const server = new GraphServer(
                '1234',
                {}
            );

            expect(server.port).toBe(1234);
        });

        it('should set params values', () => {
            expect(graphServer.params.project).toBe('test-project');
            expect(graphServer.params.instance).toBe('test-instance');
            expect(graphServer.params.database).toBe('test-database');
            expect(graphServer.params.mock).toBe(false);
        });
    });

    describe('buildRoute', () => {
        it('should correctly build route with endpoint', () => {
            const route = graphServer.buildRoute('/test-endpoint');
            expect(route).toBe('http://localhost:8000/test-endpoint');
        });

        it('should build a route to accomodate Vertex AI', () => {
            const originalLocation = window.location;
            // @ts-ignore
            delete window.location;
            window.location = { ...originalLocation, hostname: 'vertex-ai-workbench' };
            const route = graphServer.buildRoute('/test-endpoint');
            expect(route).toBe('/proxy/8000/test-endpoint');

            window.location = originalLocation;
        });
    });

    describe('query', () => {
        const mockDataPath = path.join(__dirname, '../mock-data.json');
        const mockData = JSON.parse(fs.readFileSync(mockDataPath, 'utf8'));

        beforeEach(() => {
            mockFetch.mockImplementation(() =>
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve(mockData)
                })
            );
        });

        it('should make POST request with correct parameters', async () => {
            const queryString = 'SELECT * FROM test';
            await graphServer.query(queryString);

            expect(mockFetch).toHaveBeenCalledWith(
                'http://localhost:8000/post_query',
                {
                    method: 'POST',
                    body: JSON.stringify({
                        query: queryString,
                        params: {
                            'project': 'test-project',
                            'instance': 'test-instance',
                            'database': 'test-database',
                            'mock': false
                        }
                    })
                }
            );
        });

        it('should parse the response', async () => {
            const queryString = 'SELECT * FROM test';
            const response = await graphServer.query(queryString);

            expect(response).toEqual(mockData);
        });

        it('should handle network errors', async () => {
            const errorMessage = 'Network error';
            mockFetch.mockImplementation(() => Promise.reject(new Error(errorMessage)));
            console.error = jest.fn();

            await graphServer.query('SELECT * FROM test');
            expect(console.error).toHaveBeenCalled();
        });

        it('should handle non-ok response', async () => {
            mockFetch.mockImplementation(() =>
                Promise.resolve({
                    ok: false
                })
            );
            console.error = jest.fn();

            await graphServer.query('SELECT * FROM test');
            expect(console.error).toHaveBeenCalled();
        });

        it('should set isFetching flag during request', async () => {
            const queryPromise = graphServer.query('SELECT * FROM test');
            expect(graphServer.isFetching).toBe(true);
            await queryPromise;
            expect(graphServer.isFetching).toBe(false);
        });

        it('should handle Colab environment', async () => {
            // @ts-ignore
            global.google = {
                colab: {
                    kernel: {
                        invokeFunction: jest.fn().mockResolvedValue({
                            data: {
                                'application/json': {data: 'test-response'}
                            }
                        })
                    }
                }
            };

            const result = await graphServer.query('SELECT * FROM test');
            expect(result).toEqual({data: 'test-response'});
            // @ts-ignore
            delete global.google;
        });
    });

    describe('ping', () => {
        beforeEach(() => {
            mockFetch.mockImplementation(() =>
                Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({status: 'ok'})
                })
            );
            console.log = jest.fn();
        });

        it('should make GET request to ping endpoint', async () => {
            await graphServer.ping();
            expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/get_ping');
        });
    });
});