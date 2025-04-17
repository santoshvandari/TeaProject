@extends('layouts.app')
@section('title')
    Scan Plant - KrishiConnect
@endsection
@section('breadcrumbs')
    Scan Plant
@endsection
@section('content')
 
                    <tr>
                        <td>{{$party['name']}}</td>
                        <td>{{$party['address']}}</td>
                        <td>{{$party['phone']}}</td>
                        <td>{{$party['pan']}}</td>
                        @if($party['isDealer'] )
                            <td>Dealer</td>
                        @else
                            <td>
                              Non-Dealer
                            </td>
                        @endif
                        <td>
                            <a href="/parties/{{$party['_id']}}" class="btn btn-sm btn-outline-secondary" title="Edit">
                                <i class="fas fa-edit"></i></a>

                            <form action="{{ route('parties.destroy', $party['_id']) }}" method="POST"
                                  style="display:inline;">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="btn btn-sm btn-outline-secondary"
                                        onclick="return confirm('Are you sure?')" title="Delete"><i
                                        class="fas fa-trash-alt fa-fw"></i></button>
                            </form>
                        </td>
                    </tr>
                @endforeach
                </tbody>
            </table>
        </div>
        <!-- /.card-body -->
    </div>
@endsection
