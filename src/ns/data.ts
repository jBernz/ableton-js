import { Ableton } from "..";
import { Namespace } from ".";

export interface GettableProperties {
    loops: Object[];
    fx: Object[];
    has_empty_loops: boolean;
}

export interface TransformedProperties {
}

export interface SettableProperties {
}

export interface ObservableProperties {
}

export interface RawData {
    loops: Object[];
    fx: Object[];
    has_empty_loops: boolean;
}

export class Scene extends Namespace<
    GettableProperties,
    TransformedProperties,
    SettableProperties,
    ObservableProperties
    > {
    constructor(ableton: Ableton, public raw: RawData) {
        super(ableton, "data");
    }
}
