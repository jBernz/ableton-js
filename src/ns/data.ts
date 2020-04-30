import { Ableton } from "..";
import { Namespace } from ".";

interface loopData {
    key_name: string;
    color: string;
}

interface fxData {
    name: string;
    color: string;
}

interface cbordData {
    name: string;
    color: string;
}

export interface GettableProperties {
    loops: loopData[];
    fx: fxData[];
    cbord: cbordData[];
    has_empty_loops: boolean;
}

export interface TransformedProperties {
}

export interface SettableProperties {
}

export interface ObservableProperties {
}

export interface RawData {
    loops: loopData[];
    fx: fxData[];
    cbord: cbordData[];
    has_empty_loops: boolean;
}

export class Data extends Namespace<
    GettableProperties,
    TransformedProperties,
    SettableProperties,
    ObservableProperties
    > {
    constructor(ableton: Ableton, public raw: RawData) {
        super(ableton, "data");
    }
}